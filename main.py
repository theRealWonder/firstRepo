from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton,QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDialog
from PyQt5.QtGui import QFont


# setting
app = QApplication([])
mainWindow = QWidget()
mainWindow.setWindowTitle("Todo App")
mainWindow.resize(900, 900)
dialogOpen = False



#widgets

addTask = QPushButton("Add Task")


# create a new screen where we can add tasks
def createWidget():
    global dialogOpen

    if dialogOpen:
        return

    def close():
        global dialogOpen
        box.close()
        dialogOpen = False
        return
    
    def save():
        global dialogOpen
        headert = header.text()
        description = textArea.text()
        with open('data.txt', 'a') as file:
            file.write("Header: " + headert + "\n")
            file.write("Description: " + description + "\n" + "\n")
        box.close()
        dialogOpen = False
        return


    box = QDialog()
    box.setStyleSheet("QDialog{background-color: black}")
    box.setWindowFlags(Qt.FramelessWindowHint)
    layout = QVBoxLayout()
    header = QLineEdit()
    textArea = QLineEdit()
    buttonC = QPushButton("Cancel")
    buttonS = QPushButton("Save")

    row1 = QVBoxLayout()
    row2 = QVBoxLayout()
    row3 = QHBoxLayout()

    row1.addWidget(header)
    row2.addWidget(textArea)
    row3.addWidget(buttonC)
    row3.addWidget(buttonS)


    layout.addLayout(row1)
    layout.addLayout(row2)
    layout.addLayout(row3)
    box.setLayout(layout)

    dialogOpen = True

    buttonC.clicked.connect(close)
    buttonS.clicked.connect(save)

    box.show()
    box.exec_()








addTask.clicked.connect(createWidget)



def loadTask():
    layoutTask = QVBoxLayout()

    with open('data.txt', 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 3):
        if i+1 < len(lines):
            header = lines[i].strip()
            description = lines[i+1].strip()

            headerLabel = QLabel(header)
            descriptionLabel = QLabel(description)
            delete = QPushButton("Delete")

            headerLabel.setStyleSheet("font-weight: bolder; color: white;")
            descriptionLabel.setStyleSheet("font-weight: bold; color: white;")
            delete.setStyleSheet("font: bold; background-color: red; color: white; width: fit-content;")

            delete.clicked.connect(lambda checked, header=header: deleteTask(header))

            containerWidget = QWidget()
            containerLayout = QHBoxLayout()
            col1 = QVBoxLayout()
            col2 = QVBoxLayout()

            col1.addWidget(headerLabel)
            col1.addWidget(descriptionLabel)

            col2.addWidget(delete)

            containerLayout.addLayout(col1)
            containerLayout.addLayout(col2)

            containerWidget.setLayout(containerLayout)

            containerWidget.setStyleSheet("""
                background-color: black;
                padding: 10px;
                margin-bottom: 10px;
                border: 2px solid black;
                border-radius: 5px;
                """)
            
            layoutTask.addWidget(containerWidget)

    masterLayout.addLayout(layoutTask)



def deleteTask(headerToDelete):
    # Read all lines from the file
    with open('data.txt', 'r') as file:
        lines = file.readlines()

    # Filter out the lines that match the task to delete
    new_lines = []
    skip_next = False
    for i in range(0, len(lines), 3):
        if i + 1 < len(lines):
            header = lines[i].strip()
            if header != headerToDelete:
                new_lines.append(lines[i])
                new_lines.append(lines[i + 1])
            else:
                skip_next = True  # Skip this task's 3 lines
        if skip_next:
            skip_next = False  # Skip the description and delete button for this task

    # Rewrite the file with the new content (after deletion)
    with open('data.txt', 'w') as file:
        file.writelines(new_lines)

    # Reload the tasks to reflect the deletion
    reloadTasks()


# Reload all tasks after deletion to update the UI
def reloadTasks():
    # Clear the current layout
    for i in reversed(range(masterLayout.count())):
        widget = masterLayout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()

    # Load the tasks again to refresh the layout
    loadTask()

# layout


masterLayout = QVBoxLayout()

row = QHBoxLayout()

row.addWidget(addTask)

masterLayout.addLayout(row, 0)




mainWindow.setLayout(masterLayout)

loadTask()


# show


mainWindow.show()
app.exec_()

