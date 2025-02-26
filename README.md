# Creating a mask manually for Flux and Stable Diffusion inpainting piplines.
#### Python and PyGame
### For inpainting piplines in diffusers library you need apply for entry both image and mask. Models may not detect masks correctly. Here I can offer a solution on how to make a mask yourself if the model can't handle it.

### Steps for installation:
* 1)Clone the repo
* 2)Install venv using pip(for Windows: python -m venv venv; for Linux: python3 -m venv venv)
* 3)Actvate venv(for Windows: .\venv\Scripts\activate; for Linux: source venv/bin/activate)
* 4)Install Requirments.txt
* 5)Place in the project the photo for which we want to make a mask
* 6)Run project

### Control commands
* Left click to drow
* Right click to erase
* Mouse wheel to resize brush
* Ctr+wheel to zoom
* Middle click to pan
* Enter to save

#### Init image
![image-4](https://github.com/user-attachments/assets/c0cb87f1-521e-4f66-baaa-7cc86b78d9e6)

### Mask image
![image-4](https://github.com/user-attachments/assets/4b7f873a-b8ad-4f17-9840-b1fcce4c8788)
