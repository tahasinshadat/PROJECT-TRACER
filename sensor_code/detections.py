import uv_sensor
import ir_sensor
import temp_sensor
import gas_sensor
import humidity_sensor

def is_fire():
    uv_value = uv_sensor.read_uv_sensor()
    ir_value = ir_sensor.read_ir_sensor()
    temp_value = temp_sensor.read_temp_sensor()

    uv_threshold = 0
    ir_threshold = 0
    temp_threshold = 0

    if uv_value > uv_threshold or ir_value > ir_threshold or temp_value > temp_threshold:
        print("Fire Detected")

def is_amonia():
    gas_value = gas_sensor.read_gas_sensor()

    ammonia_threshold = 0

    if gas_value > ammonia_threshold:
        print("Ammonia Detected")

def is_carbon_monoxide():
    gas_value = gas_sensor.read_gas_sensor()

    co_threshold = 0

    if gas_value > co_threshold:
        print("Carbon Monoxide Detected")

def is_nitrous():
    gas_value = gas_sensor.read_gas_sensor()

    nitrous_threshold = 0 

    if gas_value > nitrous_threshold:
        print("Nitrous Detected")

# is_fire()
# is_amonia()
# is_carbon_monoxide()
# is_nitrous()