# LoCoQuad_PCA9685_tester

Fast servo tester for LoCoQuad Robot: https://github.com/TomBlackroad/LoCoQuad

run: "python motor_tester.py" for instructions

run: "python motor_tester.py <servo_id> <angle>" to execute servo movements.
  
For the LoCoQuad Robot: servo_id = 0-7 and angle = 0-180 [WARNING]: Some joint have reduced range of motion due to mechanical construction. Always start with "angle = 90" 

We hope you find this script useful. Please give us some feedback so we can improve.
