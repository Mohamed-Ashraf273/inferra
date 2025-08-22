# 🚀 Inferra

**Inferra** is an open-source platform for hosting, sharing, and running **pre-trained Machine Learning, Deep Learning, and NLP models**.  
It provides a simple and interactive UI to explore models, make predictions, and deploy them with ease, making model inference accessible to teams, researchers, and enthusiasts alike.

We are a group of students from the **Faculty of Engineering, Cairo University**, working to make AI models **easy to use, share, and deploy**.

---

## 🌟 Why Inferra?

- **Central Model Hub** – Store and manage all your models in one convenient place.  
- **Easy Inference** – Run predictions from the UI with minimal setup.  
- **Deployment Ready** – Seamlessly deploy models for production or research use.  
- **Framework Agnostic** – Compatible with **PyTorch** and **TensorFlow** frameworks.  
- **Community Driven** – Share models, ideas, and improvements with the AI community.  

---

## 🎯 Our Vision

To create a platform where AI models can be **easily hosted, explored, and used**, empowering researchers, developers, and enthusiasts to leverage AI **without the overhead of setup or integration**.

---

## 🚀 Run the App (For Everyone)

If you just want to **try Inferra** without setting up the development environment, you can run the app directly here:  

👉 [Inferra Live App](https://inferra-git.streamlit.app/)

---

## 🛠️ Contribution Guide (For Developers)

We welcome contributions from everyone — whether you want to improve the platform, add new models, or help with documentation. Here’s how you can get started:

### How to Contribute

1. **Fork the repository** and create your branch from `main`.
2. **Clone your fork** and set up the development environment:
    ```bash
    git clone https://github.com/your-username/inferra.git
    cd inferra
    pip install -r requirements.txt
    ```
3. **Create a new branch** for your feature or bugfix:
    ```bash
    git checkout -b my-feature
    ```
4. **Make your changes**, following these guidelines:
    - Add new **model architectures** in `src/models` using `torch_model` or `tensorflow_model`.  
    - If you create **new layers**, add them under `src/layers/`.  
    - Create your own app in `app/apps` if necessary.  
    - Upload trained model weights to cloud storage (Google Drive, AWS S3, etc.) — **do not include large model files in the repo**.  

5. **Commit and push** your changes:
    ```bash
    pre-commit run --all-files --hook-stage manual
    git add .
    git commit -m "Describe your changes"
    git push origin my-feature
    ```
6. **Open a Pull Request** on GitHub and describe your changes clearly.

---

## 💡 Get Involved

- Add new pre-trained models or layers.  
- Improve the web interface and UX.  
- Help with documentation and tutorials.  
- Test the platform and provide feedback.


---

Happy coding! 🚀  
**Join the Inferra community and help make AI accessible for everyone!**
