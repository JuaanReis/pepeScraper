"""
    Function that returns a random IP address.

    **Author:** JuaanReis       
    **Date:** 21-11-2025        
    **Last modification:** -          
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:** 1.1.6            

    **Example:**    
    ```python
        from src.utils.ip_creator import get_ip
        
        print(get_ip())
    ```
"""

from random import randint

def get_ip() -> str:
    return ".".join(str(randint(1, 255)) for _ in range(4))

if __name__ == "__main__":
    print(get_ip())