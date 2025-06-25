import streamlit as st
import subprocess

st.title("APS Fault Detection - Interactive UI")

st.header("Training Pipeline")
if st.button("Run Training Pipeline"):
    with st.spinner("Running training pipeline..."):
        try:
            # Run the training pipeline as a module
            result = subprocess.run(
                ["python", "-m", "sensor.pipelines.training_pipeline"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                st.success("Training pipeline completed successfully!")
            else:
                st.error(f"Training pipeline failed!\n{result.stderr}")
        except Exception as e:
            st.error(f"Error running training pipeline: {e}")

# Optional: Batch prediction UI
st.header("Batch Prediction (Optional)")
uploaded_file = st.file_uploader("Upload CSV for batch prediction", type=["csv"])
if uploaded_file is not None:
    import os
    import tempfile

    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    with st.spinner("Running batch prediction..."):
        try:
            from sensor.pipelines.batch_prediction import start_batch_prediction

            output_path = start_batch_prediction(input_path)
            st.success("Batch prediction completed!")
            with open(output_path, "rb") as f:
                st.download_button(
                    "Download Predictions", f, file_name=os.path.basename(output_path)
                )
        except Exception as e:
            st.error(f"Batch prediction failed: {e}")
