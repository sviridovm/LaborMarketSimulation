import numpy as np

class MacroEvent:
    def __init__(self, name, effect_func):
        self.name = name
        self.effect_func = effect_func

    def apply(self, labor_market, time):
        self.effect_func(labor_market, time)
        
        



# fluctuates between 0% and 3%, period of 12 months 
def inflation_function(labor_market, month):
    rate = np.sin(2 * np.pi * month / 12) * 0.015 + 0.015
    noise = np.random.normal(-.015, 0.015)
    rate += noise
    
    rate = max(rate, 0)
    
    for worker in labor_market.get_workers():
        worker.adjusted_COL *= (1 + rate)
        worker.worker_log.append(f"COL adjusted by {rate} due to inflation")
    
inflation = MacroEvent("Inflation", inflation_function)
