from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageCms
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Конфигурация
UPLOAD_FOLDER = 'uploads'
PREVIEW_FOLDER = 'previews'
PROFILE_FOLDER = 'profiles'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREVIEW_FOLDER, exist_ok=True)
os.makedirs(PROFILE_FOLDER, exist_ok=True)

print("✅ Сервер запускается...")
print(f"   Pillow версия: {Image.__version__}")

try:
    from PIL import features
    icc_supported = features.check('littlecms2') or features.check('lcms2')
    print(f"   LittleCMS поддержка: {'ДА' if icc_supported else 'НЕТ'}")
except:
    icc_supported = False
    print("   Не удалось проверить поддержку ICC")

icc_profiles = {}
if icc_supported:
    print("\nЗагрузка ICC профилей...")
    
    icc_profiles['srgb'] = ImageCms.createProfile("sRGB")
    print("   sRGB профиль создан")
    
   
    cmyk_profiles = {
        'coated': 'coated.icc', 
        'uncoated': 'uncoated.icc',     
    }
    
    for name, filename in cmyk_profiles.items():
        profile_path = os.path.join(PROFILE_FOLDER, filename)
        if os.path.exists(profile_path):
            icc_profiles[name] = ImageCms.getOpenProfile(profile_path)
            print(f"   ✅ Загружен CMYK профиль: {name} ({filename})")
        else:
            print(f"   ⚠️ Профиль {name} не найден: {profile_path}")
    
    if len(icc_profiles) == 1:  # только sRGB
        print("\n⚠️ НЕТ CMYK профилей! Скачайте их.")


def rgb_to_cmyk_simple(r, g, b):
    """
    Простая математическая конвертация RGB в CMYK
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    k = 1 - max(r, g, b)
    
    if k == 1:
        return 0.0, 0.0, 0.0, 100.0
    
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    
    return round(c * 100, 1), round(m * 100, 1), round(y * 100, 1), round(k * 100, 1)


def cmyk_to_rgb_approx(c, m, y, k):
    """Обратная конвертация CMYK → RGB для визуального превью"""
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)



@app.route('/convert-image-icc', methods=['POST'])
def convert_image_icc():
    """
    Конвертация изображения RGB → CMYK с использованием ICC профилей
    """
    if not icc_supported:
        return jsonify({
            "error": "ICC-профили не поддерживаются. Установите Pillow с LittleCMS"
        }), 500
    
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        profile_name = request.form.get('profile', 'coated')
        
        if profile_name not in icc_profiles:
            return jsonify({
                "error": f"Profile '{profile_name}' not available",
                "available": [k for k in icc_profiles.keys() if k != 'srgb']
            }), 400


        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_input{os.path.splitext(filename)[1]}")
        output_path = os.path.join(PREVIEW_FOLDER, f"{unique_id}_preview_icc.jpg")
        
        file.save(input_path)
        
        img = Image.open(input_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        
        transform = ImageCms.buildTransform(
            icc_profiles['srgb'],        
            icc_profiles[profile_name], 
            "RGB",                        
            "CMYK"                        
        )
        
        img_converted = ImageCms.applyTransform(img, transform)

        preview_transform = ImageCms.buildTransform(
            icc_profiles[profile_name],  # из CMYK
            icc_profiles['srgb'],         # в sRGB
            "CMYK", "RGB"
        )
        img_preview = ImageCms.applyTransform(img_converted, preview_transform)
        
        img_preview.save(output_path, 'JPEG', quality=92)
        
        
        return send_file(output_path, mimetype='image/jpeg')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/health', methods=['GET'])
def health():
    """Проверка работоспособности сервера"""
    available_profiles = [k for k in icc_profiles.keys() if k != 'srgb']
    
    return jsonify({
        "status": "ok",
        "pillow_version": Image.__version__,
        "littlecms_supported": icc_supported,
        "profiles_available": available_profiles,
        "conversion_methods": ["simple_mathematical"] + (["icc_profiles"] if icc_supported and available_profiles else [])
    })


@app.route('/convert-color', methods=['POST'])
def convert_color():
    """Конвертация одиночного цвета RGB → CMYK"""
    try:
        data = request.get_json()
        
        if not data or 'r' not in data or 'g' not in data or 'b' not in data:
            return jsonify({"error": "Missing r, g, b values"}), 400
        
        r, g, b = data['r'], data['g'], data['b']
        
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            return jsonify({"error": "RGB values must be 0-255"}), 400
        
        c, m, y, k = rgb_to_cmyk_simple(r, g, b)
        
        c_norm, m_norm, y_norm, k_norm = c/100, m/100, y/100, k/100
        r_preview, g_preview, b_preview = cmyk_to_rgb_approx(c_norm, m_norm, y_norm, k_norm)
        
        return jsonify({
            "input": {
                "rgb": {"r": r, "g": g, "b": b},
                "hex": f"#{r:02x}{g:02x}{b:02x}"
            },
            "output": {
                "cmyk": {"c": c, "m": m, "y": y, "k": k},
                "preview_rgb": {"r": r_preview, "g": g_preview, "b": b_preview},
                "preview_hex": f"#{r_preview:02x}{g_preview:02x}{b_preview:02x}"
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/convert-image', methods=['POST'])
def convert_image():
    """Конвертация изображения через простую формулу"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1].lower()
        unique_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_input{file_ext}")
        output_path = os.path.join(PREVIEW_FOLDER, f"{unique_id}_preview.jpg")
        
        file.save(input_path)
        
        img = Image.open(input_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        pixels = img.load()
        width, height = img.size

        result_img = Image.new('RGB', (width, height))
        result_pixels = result_img.load()

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                c, m, y_val, k = rgb_to_cmyk_simple(r, g, b)
                c_norm, m_norm, y_norm, k_norm = c/100, m/100, y_val/100, k/100
                r_new, g_new, b_new = cmyk_to_rgb_approx(c_norm, m_norm, y_norm, k_norm)
                result_pixels[x, y] = (r_new, g_new, b_new)
        
        result_img.save(output_path, 'JPEG', quality=90)
        return send_file(output_path, mimetype='image/jpeg')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upload-profile', methods=['POST'])
def upload_profile():
    """
    Загрузка ICC профиля на сервер
    """
    if 'profile' not in request.files:
        return jsonify({"error": "No profile file provided"}), 400
    
    file = request.files['profile']
    profile_name = request.form.get('name', os.path.splitext(file.filename)[0])
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    

    filename = secure_filename(file.filename)
    profile_path = os.path.join(PROFILE_FOLDER, filename)
    file.save(profile_path)
    

    try:
        profile = ImageCms.getOpenProfile(profile_path)
        icc_profiles[profile_name] = profile
        return jsonify({
            "success": True,
            "message": f"Profile '{profile_name}' uploaded and loaded",
            "profile_info": {
                "name": profile_name,
                "filename": filename,
                "path": profile_path
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to load profile: {str(e)}"
        }), 400

@app.route('/convert-color-icc', methods=['POST'])
def convert_color_icc():
    """Конвертация одиночного цвета RGB → CMYK с ICC профилем"""
    if not icc_supported:
        return jsonify({"error": "ICC не поддерживается"}), 500
    
    try:
        data = request.get_json()
        r, g, b = data['r'], data['g'], data['b']
        profile_name = data.get('profile', 'coated')
        
        if profile_name not in icc_profiles:
            return jsonify({"error": f"Профиль {profile_name} не найден"}), 400

        img = Image.new('RGB', (1, 1), (r, g, b))
        
        transform = ImageCms.buildTransform(
            icc_profiles['srgb'],
            icc_profiles[profile_name],
            "RGB", "CMYK"
        )
        img_cmyk = ImageCms.applyTransform(img, transform)
        
        cmyk_pixels = img_cmyk.getpixel((0, 0))
        c, m, y, k = [round(x / 255 * 100, 1) for x in cmyk_pixels]

        preview_transform = ImageCms.buildTransform(
            icc_profiles[profile_name],
            icc_profiles['srgb'],
            "CMYK", "RGB"
        )
        img_preview = ImageCms.applyTransform(img_cmyk, preview_transform)
        r_preview, g_preview, b_preview = img_preview.getpixel((0, 0))
        
        return jsonify({
            "input": {"r": r, "g": g, "b": b},
            "output": {
                "cmyk": {"c": c, "m": m, "y": y, "k": k},
                "preview_rgb": {"r": r_preview, "g": g_preview, "b": b_preview},
                "preview_hex": f"#{r_preview:02x}{g_preview:02x}{b_preview:02x}"
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == '__main__':
    print("\n" + "="*50)
    print("СЕРВЕР ЗАПУЩЕН")
    print("="*50)
    print("\nДоступные эндпоинты:")
    print("   GET  /health - проверка статуса")
    print("   POST /convert-color - конвертация цвета RGB→CMYK")
    print("   POST /convert-image - конвертация изображения (простая)")
    print("   POST /convert-image-icc - конвертация с ICC профилями")
    print("   POST /upload-profile - загрузка ICC профиля")
    
    if not icc_supported:
        print("\n ВНИМАНИЕ: LittleCMS не поддерживается!")
        print("   Установите Pillow с поддержкой LCMS2:")
        print("   pip uninstall Pillow")
        print("   pip install Pillow --no-cache-dir")
    
    print("\nДля работы ICC профилей:")
    print("   1. Скачайте CMYK профили (например, с https://www.color.org)")
    print("   2. Положите их в папку 'profiles/'")
    print("   3. Используйте эндпоинт /upload-profile для загрузки")
    
    print("\n" + "="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)