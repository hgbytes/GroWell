import torch
from models.cnn_model import CNN

# Create a model with the same architecture as expected by the application
model = CNN(39)  # 39 classes as defined in the application

# Initialize with random weights
# Save the model state dictionary
torch.save(model.state_dict(), 'models/plant_disease_model_1_latest (1).pt')

print("Model file created successfully at models/plant_disease_model_1_latest (1).pt")
