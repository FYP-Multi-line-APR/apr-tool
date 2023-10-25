import os
# os.environ["D4J_HOME"]= '/content/dear-auto-fix/DEAR/approach/sbfl/defects4j'
# os.environ['PATH'] += ':/content/dear-auto-fix/DEAR/approach/sbfl/defects4j/framework/bin'

print("setting up path variables")
os.environ["D4J_HOME"]= '/content/apr-tool/defects4j'
os.environ['PATH'] += ':/content/apr-tool/defects4j/framework/bin'
print("D4J_HOME:"+os.environ["D4J_HOME"])
print("PATH:"+os.environ['PATH'])