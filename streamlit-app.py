import streamlit as st
import base64
from pathlib import Path
from streamlit.components.v1 import html

st.set_page_config(layout="wide", page_title="3D Mouse Reveal Effect")

# App title and description
st.markdown("<div style='text-align: center; margin-bottom: 30px;'><h1>3D Mouse Reveal Effect</h1><p style='font-size: 1.2rem;'>Upload an image and move your mouse over it to reveal parts of the image with a 3D effect</p></div>", unsafe_allow_html=True)

# File uploader for image
uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png', 'webp'])

# Custom HTML component for mouse reveal effect
def mouse_reveal_component(image_base64, image_type):
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mouse Reveal Effect</title>
        <style>
            .parallax-container {{
                position: relative;
                width: 100%;
                height: 140vh; /* 2배로 늘린 높이 */
                overflow: hidden;
                border-radius: 10px;
                background-color: #000;
                margin: 0 auto;
            }}
            
            .parallax-image {{
                position: absolute;
                width: 110%;
                height: 110%;
                background-image: url('data:image/{image_type};base64,{image_base64}');
                background-size: cover;
                background-position: center;
                transform-style: preserve-3d;
                transition: transform 0.15s ease-out;
                top: -5%;
                left: -5%;
                box-shadow: 0 0 40px rgba(0,0,0,0.8);
            }}
            
            .image-mask {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 1);
                mask-image: radial-gradient(circle at center, transparent 0, black 80px);
                -webkit-mask-image: radial-gradient(circle at center, transparent 0, black 80px);
                pointer-events: none;
                z-index: 10;
            }}
            
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div id="parallaxContainer" class="parallax-container">
            <div id="parallaxImage" class="parallax-image"></div>
            <div id="imageMask" class="image-mask"></div>
        </div>
        
        <script>
            // Wait for DOM to be fully loaded
            document.addEventListener('DOMContentLoaded', function() {{
                setupMouseEffect();
            }});
            
            // Also try immediate setup for Streamlit
            setupMouseEffect();
            
            function setupMouseEffect() {{
                const parallaxImage = document.getElementById('parallaxImage');
                const container = document.getElementById('parallaxContainer');
                const imageMask = document.getElementById('imageMask');
                
                if (!container || !parallaxImage || !imageMask) {{
                    console.log("DOM elements not found, will retry...");
                    setTimeout(setupMouseEffect, 100);
                    return;
                }}
                
                console.log("Mouse effect setup initialized");
                
                // Maximum rotation amount (in degrees) - 강렬한 3D 효과를 위해 값 증가
                const maxRotation = 25;
                
                // Reveal radius (in pixels)
                const revealRadius = 150;
                
                // Track mouse position
                let mouseX = 0;
                let mouseY = 0;
                let mouseAbsX = 0;
                let mouseAbsY = 0;
                
                container.addEventListener('mousemove', function(e) {{
                    console.log("Mouse moved in container");
                    
                    // Get container dimensions
                    const rect = container.getBoundingClientRect();
                    
                    // Get absolute mouse position within container
                    mouseAbsX = e.clientX - rect.left;
                    mouseAbsY = e.clientY - rect.top;
                    
                    // Calculate mouse position relative to the center of the container (from -1 to 1)
                    mouseX = ((mouseAbsX) / rect.width - 0.5) * 2;
                    mouseY = ((mouseAbsY) / rect.height - 0.5) * 2;
                    
                    // Update mask position
                    updateMask(mouseAbsX, mouseAbsY);
                    
                    // Update parallax effect
                    updateTransform();
                }});
                
                container.addEventListener('mouseleave', function() {{
                    console.log("Mouse left container");
                    
                    // Reset when mouse leaves
                    mouseX = 0;
                    mouseY = 0;
                    
                    // Hide the image completely by moving mask offscreen
                    imageMask.style.maskImage = 'none';
                    imageMask.style.webkitMaskImage = 'none';
                    
                    // Reset transform
                    updateTransform();
                }});
                
                function updateMask(x, y) {{
                    // 더 선명한 경계를 위한 마스크 그라데이션 조정
                    const maskImage = `radial-gradient(circle ${{revealRadius}}px at ${{x}}px ${{y}}px, transparent 0%, rgba(0,0,0,0.3) 70%, black 100%)`;
                    imageMask.style.maskImage = maskImage;
                    imageMask.style.webkitMaskImage = maskImage;
                }}
                
                function updateTransform() {{
                    // Calculate rotation values - 더 강한 회전 효과
                    const rotateY = mouseX * maxRotation;
                    const rotateX = -mouseY * maxRotation;
                    
                    // 더 극적인 Z축 변환과 원근감을 위한 값 증가
                    const translateX = mouseX * 40; // 증가된 X축 이동
                    const translateY = mouseY * 40; // 증가된 Y축 이동
                    const translateZ = 50 - Math.abs(mouseX * mouseY) * 30; // Z축 변환 추가
                    
                    // 조명 효과를 위한 그림자 조정
                    const shadowX = -mouseX * 20;
                    const shadowY = -mouseY * 20;
                    const shadowBlur = 30 + Math.abs(mouseX * mouseY) * 20;
                    const shadowOpacity = 0.5 + Math.abs(mouseX * mouseY) * 0.3;
                    
                    // 그림자 효과 적용
                    parallaxImage.style.boxShadow = `${{shadowX}}px ${{shadowY}}px ${{shadowBlur}}px rgba(0,0,0,${{shadowOpacity}})`;
                    
                    // 향상된 3D 변환 적용
                    parallaxImage.style.transform = 
                        `perspective(1000px) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) translateX(${{translateX}}px) translateY(${{translateY}}px) translateZ(${{translateZ}}px)`;
                }}
                
                // Initialize mask
                imageMask.style.maskImage = 'none';
                imageMask.style.webkitMaskImage = 'none';
                
                console.log("Mouse effect setup complete");
            }}
        </script>
    </body>
    </html>
    """
    return html_code

# Process uploaded image
if uploaded_file is not None:
    # Get file content and encode as base64
    file_bytes = uploaded_file.getvalue()
    file_type = uploaded_file.type.split('/')[-1]
    base64_img = base64.b64encode(file_bytes).decode()
    
    # Display component with uploaded image
    html_component = mouse_reveal_component(base64_img, file_type)
    html(html_component, height=1400)  # 높이 증가 (2배로)
    
    st.info("👆 Move your mouse over the black area above to reveal parts of the image with an enhanced 3D effect.")
else:
    # Display placeholder
    st.info("👆 Please upload an image to see the effect.")

# Additional instructions
st.markdown("""
### How it works

1. Upload your image using the file uploader above
2. Move your mouse over the black area to reveal parts of the image
3. Notice the enhanced 3D effect as the image shifts with depth and perspective
""")

# Display technical details in expander
with st.expander("Technical Details"):
    st.markdown("""
    This app uses several advanced techniques:
    
    - **CSS Masks**: To reveal only the portion of the image near your mouse cursor
    - **Enhanced 3D Transforms**: Using perspective, rotation, and Z-axis translation for a stronger depth effect
    - **Dynamic Shadows**: Shadows that change based on mouse movement to enhance the 3D appearance
    - **Streamlit Components**: To embed the custom HTML and JavaScript in a Streamlit app
    
    The effect combines multiple transformations:
    1. A radial gradient mask reveals the image only around your cursor
    2. X and Y axis rotations tilt the image based on cursor position
    3. Z-axis translation creates a "popping out" effect as if the image is emerging from the screen
    4. Dynamic shadows reinforce the 3D illusion by simulating lighting
    """)
