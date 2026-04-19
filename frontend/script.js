const API_URL = "https://o0s85xmv5c.execute-api.us-west-2.amazonaws.com/recipe";

async function uploadImage() {
    const file = document.getElementById("imageInput").files[0];

    if (!file) {
        alert("Please select an image");
        return;
    }

    // reset previous results
    document.getElementById("recipe-name").textContent = "";
    document.getElementById("ingredients-output").textContent = "";
    document.getElementById("instructions-output").textContent = "";
    const mealThumb = document.getElementById("mealThumb");
    mealThumb.src = "";
    mealThumb.classList.add("placeholder");

    const reader = new FileReader();

    reader.onload = async function () {
        const base64Image = reader.result.split(",")[1];

        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                image: base64Image,
                filename: file.name
            })
        });

        const data = await res.json();
        const recipe = data.recipe;

        if (recipe) {
            document.getElementById("recipe-name").textContent = recipe.name
                    ? recipe.name.replace(/\b\w/g, c => c.toUpperCase())
                    : "";

            document.getElementById("ingredients-output").textContent =
                Array.isArray(recipe.ingredients)
                    ? recipe.ingredients.join("\n")
                    : "";

            document.getElementById("instructions-output").textContent =
                recipe.instructions
                    ? recipe.instructions.replace(/step\s+(\d+)/gi, (match, num) => `STEP ${num}:`)
                    : "";
        }

        if (data.recipe && data.recipe.thumbnail) {
            const mealThumb = document.getElementById("mealThumb");
            mealThumb.src = data.recipe.thumbnail;
            mealThumb.style.display = "block";
        }
    };

    reader.readAsDataURL(file);
}

document.getElementById("imageInput").addEventListener("change", function() {
    const file = this.files[0];
    if (!file) return;

    const preview = document.getElementById("preview");
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
});
