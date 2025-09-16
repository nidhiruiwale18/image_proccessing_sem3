document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) {
    alert("Please select an image.");
    return;
  }
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const response = await fetch("http://localhost:5000/upload", {
    method: "POST",
    body: formData
  });
  const data = await response.json();
  if (data.result) {
    document.getElementById("result").innerHTML =
      `<p>Reconstructed Image:</p>
       <img src="http://localhost:5000/${data.result}" alt="Reconstruction" width="300">`;
  } else {
    alert("Error: " + data.error);
  }
});
