const API_URL = 'http://localhost:5000';

let currentProfile = 'coated';

const colorPicker = document.getElementById('colorPicker');
const rgbDisplay = document.getElementById('rgbDisplay');
const cmykDisplay = document.getElementById('cmykDisplay');
const rgbValue = document.getElementById('rgbValue');
const hexValue = document.getElementById('hexValue');
const cPercent = document.getElementById('cPercent');
const mPercent = document.getElementById('mPercent');
const yPercent = document.getElementById('yPercent');
const kPercent = document.getElementById('kPercent');
const cFill = document.getElementById('cFill');
const mFill = document.getElementById('mFill');
const yFill = document.getElementById('yFill');
const kFill = document.getElementById('kFill');
const previewRgbValue = document.getElementById('previewRgbValue');
const previewHexValue = document.getElementById('previewHexValue');
const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const uploadedImage = document.getElementById('uploadedImage');



document.addEventListener('DOMContentLoaded', function() {
    checkServerHealth();
    
    if (colorPicker) {
        colorPicker.addEventListener('input', function() {
            updateColorDisplay(this.value);
            convertColorWithICC(this.value);
        });
    }
    
    const paperType = document.getElementById('paperType');
    if (paperType) {
        paperType.addEventListener('change', function() {
            currentProfile = this.value;
            const statusSpan = document.getElementById('paperStatus');
            if (statusSpan) {
                statusSpan.textContent = '🔄 пересчёт...';
            }
            if (colorPicker) {
                convertColorWithICC(colorPicker.value);
            }
            if (imageUpload && imageUpload.files.length > 0) {
                convertImageWithICC(imageUpload.files[0]);
            }
        });
    }

    if (imageUpload) {
        imageUpload.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                convertImageWithICC(file);
            }
        });
    }
    
    if (colorPicker) {
        updateColorDisplay(colorPicker.value);
        convertColorWithICC(colorPicker.value);
    }
});


function checkServerHealth() {
    fetch(`${API_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('✅ Бэкенд доступен:', data);
            if (data.littlecms_supported) {
                console.log('✅ ICC профили поддерживаются');
                const statusSpan = document.getElementById('paperStatus');
                if (statusSpan) statusSpan.textContent = '✅ ICC профиль активен';
            }
        })
        .catch(error => {
            console.error('❌ Бэкенд недоступен:', error);
            const statusSpan = document.getElementById('paperStatus');
            if (statusSpan) statusSpan.textContent = '⚠️ бэкенд не запущен';
        });
}


function updateColorDisplay(hex) {
    if (rgbDisplay) rgbDisplay.style.backgroundColor = hex;
    if (cmykDisplay) cmykDisplay.style.backgroundColor = hex;
    
    const rgb = hexToRgb(hex);
    if (rgbValue) rgbValue.textContent = `RGB(${rgb.r}, ${rgb.g}, ${rgb.b})`;
    if (hexValue) hexValue.textContent = hex.toUpperCase();
}


async function convertColorWithICC(hex) {
    const rgb = hexToRgb(hex);
    const profile = currentProfile;
    
    const statusSpan = document.getElementById('paperStatus');
    if (statusSpan) statusSpan.textContent = '🔄 конвертация...';
    
    try {
        const response = await fetch(`${API_URL}/convert-color-icc`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                r: rgb.r, 
                g: rgb.g, 
                b: rgb.b,
                profile: profile
            })
        });
        
        const data = await response.json();
        
        if (statusSpan) statusSpan.textContent = '✅ готово';
        
        if (data.error) {
            console.error('Ошибка:', data.error);
            convertColorSimple(hex);
            return;
        }
        
        updateCmykDisplay(data.output);
        
    } catch (error) {
        console.error('Ошибка ICC:', error);
        if (statusSpan) statusSpan.textContent = '⚠️ ошибка';
        convertColorSimple(hex);
    }
}


async function convertColorSimple(hex) {
    const rgb = hexToRgb(hex);
    
    try {
        const response = await fetch(`${API_URL}/convert-color`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ r: rgb.r, g: rgb.g, b: rgb.b })
        });
        
        const data = await response.json();
        
        if (!data.error) {
            updateCmykDisplay(data.output, true);
        }
    } catch (error) {
        console.error('Ошибка простой конвертации:', error);
    }
}


function updateCmykDisplay(output, isFallback = false) {
    const { cmyk, preview_rgb, preview_hex } = output;
    
    if (cPercent) cPercent.textContent = `${cmyk.c}%`;
    if (mPercent) mPercent.textContent = `${cmyk.m}%`;
    if (yPercent) yPercent.textContent = `${cmyk.y}%`;
    if (kPercent) kPercent.textContent = `${cmyk.k}%`;
    
    if (cFill) cFill.style.width = `${cmyk.c}%`;
    if (mFill) mFill.style.width = `${cmyk.m}%`;
    if (yFill) yFill.style.width = `${cmyk.y}%`;
    if (kFill) kFill.style.width = `${cmyk.k}%`;
    
    if (cmykDisplay) cmykDisplay.style.backgroundColor = preview_hex;
    if (previewRgbValue) previewRgbValue.textContent = `RGB(${preview_rgb.r}, ${preview_rgb.g}, ${preview_rgb.b})`;
    if (previewHexValue) previewHexValue.textContent = preview_hex.toUpperCase();

    const totalInk = cmyk.c + cmyk.m + cmyk.y + cmyk.k;
    const disclaimer = document.querySelector('.converter-disclaimer');
    if (disclaimer && totalInk > 240) {
        let warning = disclaimer.querySelector('.ink-warning');
        if (!warning) {
            warning = document.createElement('div');
            warning.className = 'ink-warning';
            disclaimer.appendChild(warning);
        }
        warning.style.color = '#e74c3c';
        warning.style.marginTop = '8px';
        warning.style.fontWeight = '600';
        warning.innerHTML = `Сумма чернил: ${totalInk}% (выше 240% - риск засушивания)`;
    } else if (disclaimer) {
        const warning = disclaimer.querySelector('.ink-warning');
        if (warning) warning.remove();
    }
}


async function convertImageWithICC(file) {
    if (!file.type.match('image.*')) {
        alert('Пожалуйста, выберите изображение');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {

            const container = imagePreview;
            const maxWidth = 400;
            const maxHeight = 300;
            
            let width = img.width;
            let height = img.height;

            if (width > maxWidth) {
                height = (height * maxWidth) / width;
                width = maxWidth;
            }
            if (height > maxHeight) {
                width = (width * maxHeight) / height;
                height = maxHeight;
            }
            
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = width;
            tempCanvas.height = height;
            const tempCtx = tempCanvas.getContext('2d');
            tempCtx.drawImage(img, 0, 0, width, height);

            uploadedImage.style.width = `${width}px`;
            uploadedImage.style.height = `${height}px`;
            uploadedImage.style.objectFit = 'contain';
            uploadedImage.src = tempCanvas.toDataURL();
            imagePreview.style.display = 'block';
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
 
    const formData = new FormData();
    formData.append('image', file);
    formData.append('profile', currentProfile);
    
    imagePreview.classList.add('loading');
    
    try {
        const response = await fetch(`${API_URL}/convert-image-icc`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Ошибка сервера');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        const resultImg = new Image();
        resultImg.onload = function() {
            const container = imagePreview;
            const maxWidth = 400;
            const maxHeight = 300;
            
            let width = resultImg.width;
            let height = resultImg.height;
            
            if (width > maxWidth) {
                height = (height * maxWidth) / width;
                width = maxWidth;
            }
            if (height > maxHeight) {
                width = (width * maxHeight) / height;
                height = maxHeight;
            }
            
            uploadedImage.style.width = `${width}px`;
            uploadedImage.style.height = `${height}px`;
            uploadedImage.src = url;
        };
        resultImg.src = url;
        
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при конвертации изображения: ' + error.message);
    } finally {
        imagePreview.classList.remove('loading');
    }
}


function hexToRgb(hex) {
    hex = hex.replace('#', '');
    if (hex.length === 3) {
        hex = hex.split('').map(c => c + c).join('');
    }
    return {
        r: parseInt(hex.substring(0, 2), 16),
        g: parseInt(hex.substring(2, 4), 16),
        b: parseInt(hex.substring(4, 6), 16)
    };
}

console.log('Фронтенд загружен, API URL:', API_URL);