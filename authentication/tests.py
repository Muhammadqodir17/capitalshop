a = 'root1234'
if not any(char.isdigit() for char in a) or not any(char in a for char in '_.'):
    pass

print(any(char.isdigit() for char in a))
print(any(char in a for char in '_.'))
