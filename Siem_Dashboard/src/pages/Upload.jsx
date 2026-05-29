import { useState } from "react";

function Upload() {
  const [file, setFile] = useState(null);

  function handleFileChange(e) {
    setFile(e.target.files[0]);
  }

  function handleUpload() {
    if (!file) {
      alert("Vælg en fil først");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        console.log("Upload success:", data);
        alert("Uploadet!");
      })
      .catch(err => {
        console.error("Error:", err);
        alert("Fejl ved upload");
      });
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Upload Logs</h1>

      <input type="file" onChange={handleFileChange} />
      <br /><br />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default Upload;