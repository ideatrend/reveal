import streamlit as st
import base64
from pathlib import Path

st.set_page_config(layout="wide", page_title="3D Mouse Reveal Effect")

# Custom CSS and JavaScript for the mouse reveal effect
def get_js_code():
    return """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const parallaxImage = document.getElementById('parallaxImage');
        const container = document.getElementById('parallaxContainer');
        const imageMask = document.getElementById('imageMask');
        
        // Maximum rotation amount (in degrees)
        const maxRotation = 10;
        
        // Reveal radius (in pixels)
        const revealRadius = 100;
        
        // Track mouse position
        let mouseX = 0;
        let mouseY = 0;
        let mouseAbsX = 0;
        let mouseAbsY = 0;
        
        if (container) {
            container.addEventListener('mousemove', function(e) {
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
            });
            
            container.addEventListener('mouseleave', function() {
                // Reset when mouse leaves
                mouseX = 0;
                mouseY = 0;
                
                // Hide the image completely by moving mask offscreen
                if (imageMask) {
                    imageMask.style.maskImage = 'none';
                    imageMask.style.webkitMaskImage = 'none';
                }
                
                // Reset transform
                updateTransform();
            });
        }
        
        function updateMask(x, y) {
            // Make sure imageMask exists
            if (imageMask) {
                // Update mask to reveal image only around mouse position
                const maskImage = `radial-gradient(circle ${revealRadius}px at ${x}px ${y}px, transparent 0%, black 100%)`;
                imageMask.style.maskImage = maskImage;
                imageMask.style.webkitMaskImage = maskImage;
            }
        }
        
        function updateTransform() {
            // Make sure parallaxImage exists
            if (parallaxImage) {
                // Calculate rotation values
                const rotateY = mouseX * maxRotation;
                const rotateX = -mouseY * maxRotation; // Negative because we want to tilt away from mouse
                
                // Calculate translation values (parallax effect)
                const translateX = mouseX * 20; // px
                const translateY = mouseY * 20; // px
                
                // Apply transform
                parallaxImage.style.transform = 
                    `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translate(${translateX}px, ${translateY}px)`;
            }
        }
    });
    </script>
    """

def get_css_code(image_url):
    return f"""
    <style>
        /* Override some Streamlit styles for full screen effect */
        header {{
            visibility: visible !important;
            height: auto !important;
            background-color: transparent !important;
            padding-top: 10px;
        }}
        .main .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
        }}
        footer {{
            visibility: hidden;
        }}
        
        /* Our custom styles */
        .parallax-container {{
            position: relative;
            width: 100%;
            height: 80vh;
            overflow: hidden;
            border-radius: 10px;
            background-color: #000;
        }}
        
        .parallax-image {{
            position: absolute;
            width: 100%;
            height: 100%;
            background-image: url('{image_url}');
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
            background-color: rgba(0, 0, 0, 1); /* Black overlay to hide the image */
            mask-image: radial-gradient(circle at center, transparent 0, black 80px);
            -webkit-mask-image: radial-gradient(circle at center, transparent 0, black 80px);
            pointer-events: none;
            z-index: 10;
        }}
        
        .content {{
            position: relative;
            color: white;
            text-align: center;
            width: 100%;
            pointer-events: none;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .description {{
            font-size: 1.2rem;
            margin-bottom: 1rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
    </style>
    """

# Function to get image URL for CSS
def get_image_url(image_file):
    if image_file is not None:
        file_bytes = image_file.getvalue()
        base64_img = base64.b64encode(file_bytes).decode()
        return f"data:image/{image_file.type.split('/')[-1]};base64,{base64_img}"
    else:
        # Return a placeholder image if no file is uploaded
        return "https://via.placeholder.com/1920x1080.png?text=Upload+an+image"

# App title and description
st.markdown("<div class='content'><h1>3D Mouse Reveal Effect</h1><p class='description'>Upload an image and move your mouse over it to reveal parts of the image with a 3D effect</p></div>", unsafe_allow_html=True)

# File uploader for image
uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png', 'webp'])

# Get image URL
image_url = get_image_url(uploaded_file)

# Insert HTML, CSS and JavaScript
st.markdown(get_css_code(image_url), unsafe_allow_html=True)
st.markdown(f"""
    <div id="parallaxContainer" class="parallax-container">
        <div id="parallaxImage" class="parallax-image"></div>
        <div id="imageMask" class="image-mask"></div>
    </div>
    {get_js_code()}
""", unsafe_allow_html=True)

# Additional instructions
st.markdown("""
### How it works
1. Upload your image using the file uploader above
2. Move your mouse over the black area to reveal parts of the image
3. Notice the 3D effect as the image shifts with your mouse movement

""")
