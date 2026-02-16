/**
 * Main Background Remover Logic
 * API: https://background-remover-2tc2.onrender.com
 */

const API_URL = "https://background-remover-2tc2.onrender.com/remove-bg";

async function removeBackground() {
    const fileInput = document.getElementById('imageInput');
    const resultImage = document.getElementById('resultImage');
    const uploadBtn = document.querySelector('button');
    const loadingText = document.getElementById('loadingText');

    // 1. Validation
    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Please select an image file first.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    // 2. UI Feedback (Loading state)
    uploadBtn.disabled = true;
    uploadBtn.innerText = "Processing...";
    if (loadingText) loadingText.style.display = "block";
    resultImage.style.display = "none";

    try {
        // 3. API Call
        console.log("Sending image to AI server...");
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to process image");
        }

        // 4. Handle Response
        const blob = await response.blob();
        
        // Create a local URL for the transparent image
        const imageUrl = URL.createObjectURL(blob);
        
        // 5. Update UI
        resultImage.src = imageUrl;
        resultImage.style.display = "block";
        
        console.log("Success! Background removed.");

    } catch (error) {
        console.error("Error:", error);
        alert(`Error: ${error.message}. Make sure your Render server is awake!`);
    } finally {
        // 6. Reset UI
        uploadBtn.disabled = false;
        uploadBtn.innerText = "Remove Background";
        if (loadingText) loadingText.style.display = "none";
    }
}

// Optional: Clear memory when the user leaves the page
window.onbeforeunload = function() {
    const resultImage = document.getElementById('resultImage');
    if (resultImage.src.startsWith('blob:')) {
        URL.revokeObjectURL(resultImage.src);
    }
};