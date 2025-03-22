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
                height: 70vh;
                overflow: hidden;
                border-radius: 10px;
                background-color: #000;
                margin: 0 auto;
            }}
            
            .parallax-image {{
                position: absolute;
                width: 100%;
                height: 100%;
                background-image: url('data:image/{image_type};base64,{image_base64}');
                background-size: cover;
                background-position: center;
                transform-style: preserve-3d;
                transition: transform 0.1s ease-out;
                top: 0;
                left: 0;
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
                
                // Maximum rotation amount (in degrees)
                const maxRotation = 10;
                
                // Reveal radius (in pixels)
                const revealRadius = 100;
                
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
                    // Update mask to reveal image only around mouse position
                    const maskImage = `radial-gradient(circle ${{revealRadius}}px at ${{x}}px ${{y}}px, transparent 0%, black 100%)`;
                    imageMask.style.maskImage = maskImage;
                    imageMask.style.webkitMaskImage = maskImage;
                }}
                
                function updateTransform() {{
                    // Calculate rotation values
                    const rotateY = mouseX * maxRotation;
                    const rotateX = -mouseY * maxRotation; // Negative because we want to tilt away from mouse
                    
                    // Calculate translation values (parallax effect)
                    const translateX = mouseX * 20; // px
                    const translateY = mouseY * 20; // px
                    
                    // Apply transform
                    parallaxImage.style.transform = 
                        `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) translate(${{translateX}}px, ${{translateY}}px)`;
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
    html(html_component, height=700)
    
    st.info("👆 Move your mouse over the black area above to reveal parts of the image with a 3D effect.")
else:
    # Display placeholder
    st.info("👆 Please upload an image to see the effect.")
    
    # You could also show demo image
    # html_component = mouse_reveal_component("demo_base64_string", "jpeg")
    # html(html_component, height=700)

# Additional instructions
st.markdown("""
### How it works

1. Upload your image using the file uploader above
2. Move your mouse over the black area to reveal parts of the image
3. Notice the 3D effect as the image shifts with your mouse movement
""")

# Display technical details in expander
with st.expander("Technical Details"):
    st.markdown("""
    This app uses a combination of:
    
    - **CSS Masks**: To reveal only the portion of the image near your mouse cursor
    - **3D Transforms**: To create a parallax effect that gives depth as you move the mouse
    - **Streamlit Components**: To embed the custom HTML and JavaScript in a Streamlit app
    
    The effect works by tracking your mouse position and:
    1. Creating a radial gradient mask that only shows the image in a circle around your cursor
    2. Applying a 3D transform to the image based on mouse position
    """)
