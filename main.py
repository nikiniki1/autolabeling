import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(folder, filename)
            images.append(img_path)
    return images


def main():
    st.title("Image Annotation Service with Points")


    folder_path = st.text_input("Enter the path to the directory with images:")
    
    if folder_path and os.path.isdir(folder_path):
        images = load_images_from_folder(folder_path)
        if images:
            if 'current_index' not in st.session_state:
                st.session_state.current_index = 0

            current_image_path = images[st.session_state.current_index]
            image = Image.open(current_image_path)
            st.write(f"Image {st.session_state.current_index + 1} of {len(images)}")

            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)", 
                stroke_width=3,
                stroke_color="#FFFFFF",
                background_image=image,
                update_streamlit=True,
                height=image.height,
                width=image.width,
                drawing_mode="point", 
                key=f"canvas_{st.session_state.current_index}", 
            )

            if canvas_result.json_data is not None:
                points = canvas_result.json_data["objects"]
                if points:
                    x, y = points[0]["left"], points[0]["top"]
                    st.write(f"Point coordinates: ({x}, {y})")

                    if 'annotations' not in st.session_state:
                        st.session_state.annotations = {}
                    st.session_state.annotations[st.session_state.current_index] = (x, y)

            label = st.text_input("Enter the class label for the current image:", key="label_input")

            if st.button("Save label and coordinates"):
                if 'annotations' not in st.session_state:
                    st.session_state.annotations = {}
                if 'labels' not in st.session_state:
                    st.session_state.labels = {}

                st.session_state.labels[st.session_state.current_index] = label
                st.success(f"Label '{label}' and coordinates saved for image {current_image_path}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Previous image") and st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
            with col2:
                if st.button("Next image") and st.session_state.current_index < len(images) - 1:
                    st.session_state.current_index += 1


            if 'labels' in st.session_state and 'annotations' in st.session_state:
                st.write("Saved data:")
                for idx, (img_path, label) in enumerate(zip(images, st.session_state.labels.values())):
                    st.write(f"Image {idx + 1}: {img_path}")
                    st.write(f"Label: {label}")
                    if idx in st.session_state.annotations:
                        x, y = st.session_state.annotations[idx]
                        st.write(f"Point coordinates: ({x}, {y})")
        else:
            st.warning("No images found in the specified directory.")
    else:
        st.warning("Please enter a valid directory path.")

if __name__ == "__main__":
    main()