import socketio
import eventlet
sio = socketio.Server()
app = socketio.WSGIApp(sio)
import re
import inspect
import requests
import random
import string
import ast

api_key = "l7s5ukux5iy7i5qprh4b348xcr8tymlbvy2f7ysepcno637il"
url = f"https://api.wordnik.com/v4/words.json/randomWord?api_key={api_key}"




@sio.on('send_variable')
def receive_variable(sid, contents):
    globFilePath = contents["filePath"]
    # Do something with the variable
    if(contents["filePath"].endswith(".c") or contents["filePath"].endswith('.cpp')):
        contents = contents['fileContent']
        function_pattern = re.compile(r"void\s+(\w+)\s*\(")
        macro_pattern = re.compile(r"#define\s+(\w+)")
        variable_pattern = re.compile(r"\b(\w+)\b\s*(?:=.*|;)")

        # Find all matches of each pattern in the file
        functions = function_pattern.findall(contents)
        macros = macro_pattern.findall(contents)
        variables = variable_pattern.findall(contents)

        # Create a dictionary to store the variables and their corresponding functions/classes
        var_functions = {}
        varr = []
        # Add code to iterate through variables inside functions and classes
        module = inspect.getmodule(inspect.currentframe())
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) or inspect.isclass(obj):
                code = obj.__code__
                function_variables = set(code.co_names)
                for var in code.co_consts:
                    if inspect.iscode(var):
                        function_variables.update(var.co_names)
                        for var_name in var.co_names:
                            var_functions[var_name] = name
                for var_name in function_variables:
                    var_functions[var_name] = name

        # Print the C file outline
        print("C File Outline:")
        if functions:
            print("Functions:")
            for func in functions:    
                if len(func) > 3 and func != "return" and func != "main" and func != "break" :  
                     
                        res = ''.join(random.choices(string.ascii_letters, k=7)) 
                        contents = contents.replace(func, res) 
        if macros:
            print("Macros:")
            for macro in macros:
                if len(macro) > 3 :  
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        random_word = data["word"].replace("-", "_")
                        random_word = random_word.replace("'", "")
                        contents = contents.replace(macro, random_word)
                    else:
                        print("Failed to retrieve a random word")  
                        res = ''.join(random.choices(string.ascii_letters, k=7)) 
                        contents = contents.replace(macro, res) 
        if variables:
            print("Variables:")
            for variable in variables:
                function_name = var_functions.get(variable, None)
                if len(variable) > 3 and  variable != "break" and variable != "return" and variable != "main":  
                
                        res = ''.join(random.choices(string.ascii_letters, k=7)) 
                        contents = contents.replace(variable, res) 
                if function_name:
                    print("- " + variable + " (from function/class " + function_name + ")")
                    varr.append(variable)
                else:
                    print("- " + variable)
                    varr.append(variable)
    else :
        class OutlineVisitor(ast.NodeVisitor):
            def __init__(self):
                self.functions = []
                self.classes = []
                self.variables = {}
                self.class_variables = {}

            def visit_FunctionDef(self, node):
                self.functions.append(node.name)
                self.variables[node.name] = []

                # Visit the function body to find variables defined inside
                for child_node in ast.walk(node):
                    if isinstance(child_node, ast.Assign):
                        for target in child_node.targets:
                            if isinstance(target, ast.Name):
                                self.variables[node.name].append(target.id)

            def visit_ClassDef(self, node):
                self.classes.append(node.name)
                self.class_variables[node.name] = []

                # Visit the class body to find variables and functions defined inside
                for child_node in node.body:
                    if isinstance(child_node, ast.FunctionDef):
                        self.class_variables[node.name].append(child_node.name)
                        self.variables[child_node.name] = []
                        for sub_child_node in ast.walk(child_node):
                            if isinstance(sub_child_node, ast.Assign):
                                for target in sub_child_node.targets:
                                    if isinstance(target, ast.Name):
                                        self.variables[child_node.name].append(target.id)
                    elif isinstance(child_node, ast.Assign):
                        for target in child_node.targets:
                            if isinstance(target, ast.Name):
                                self.class_variables[node.name].append(target.id)

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    # If the name is being assigned to, add it to the list of variables
                    if node.id not in self.variables:
                        self.variables[node.id] = []
                    for func in reversed(self.functions):
                        if node.id in self.variables[func]:
                            return
                    for cls in reversed(self.classes):
                        if node.id in self.class_variables[cls]:
                            return
                    self.variables[node.id].append(None)


        contents = contents['fileContent']
        tree = ast.parse(contents)

        # Traverse the AST using the OutlineVisitor
        visitor = OutlineVisitor()
        visitor.visit(tree)

        # Print the Python file outline
        print("Python File Outline:")
        if visitor.functions:
            print("Functions:")
            for func in visitor.functions:
                if len(func) > 3 and func != "return" and func != "main" and func != "break" and func != "__init__":  
                     
                        res = ''.join(random.choices(string.ascii_letters, k=7)) 
                        contents = contents.replace(func, res) 
                print("- " + func)
                if visitor.variables.get(func):
                    print("  Variables:")
                    for var in visitor.variables[func]:
                        if len(var) > 3 and var != "break" and var != "return" and var != "main" and var != "__init__":  
                              
                                res = ''.join(random.choices(string.ascii_letters, k=7)) 
                                contents = contents.replace(var, res) 
                        print("  - " + var)
        if visitor.classes:
            print("Classes:")
            for cls in visitor.classes:
                if len(cls) > 3 and cls != "break" and cls != "return" and cls != "main" and cls != "__init__":  
                      
                        res = ''.join(random.choices(string.ascii_letters, k=7)) 
                        contents = contents.replace(cls, res) 
                print("- " + cls)
                if visitor.class_variables.get(cls):
                    print("  Variables:")
                    for var in visitor.class_variables[cls]:
                        if len(var) > 3 and var != "break" and var != "return" and var != "main" and var != "__init__":  
                              
                                res = ''.join(random.choices(string.ascii_letters, k=7)) 
                                contents = contents.replace(var, res) 
                        print("  - " + var)
                if visitor.functions:
                    print("  Functions:")
                    for func in visitor.functions:
                        if func in visitor.class_variables.get(cls, []):
                            if len(func) > 3 and func != "break" and func != "return" and func != "main" and func != "__init__":  
                                 
                                    res = ''.join(random.choices(string.ascii_letters, k=7)) 
                                    contents = contents.replace(func, res) 
                            print("  - " + func)
                            if visitor.variables.get(func):
                                print("    Variables:")
                                for var in visitor.variables[func]:
                                    if len(var) > 3 and var != "break" and var != "return" and var != "main" and var != "__init__":  
                                          
                                            res = ''.join(random.choices(string.ascii_letters, k=7)) 
                                            contents = contents.replace(var, res) 
                                    print("    - " + var)
        if visitor.variables:
            print("Variables:")
            for var in visitor.variables:
                if var not in visitor.functions and var not in visitor.classes:
                    if len(var) > 3 and var != "break" and var != "return" and var != "main" and var != "__init__":  
                          
                            res = ''.join(random.choices(string.ascii_letters, k=7)) 
                            contents = contents.replace(var, res) 
                    print("- " + var)
    sio.emit('result', {"globFilePath": globFilePath, "contents": contents}, room=sid)
    
    

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
