// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below

const vscode = require("vscode");
const path = require("path");
const { spawn } = require("child_process");
const pythonProcess = spawn("python", [path.join(__dirname, "extension.py")]);
const io = require("socket.io-client");
const { fstat } = require("fs");
const socket = io("http://localhost:5000");
const fs = require("fs");

pythonProcess.stdout.on("data", (data) => {
  console.log(`stdout: ${data}`);
});
pythonProcess.stderr.on("data", (data) => {
  console.error(`stderr: ${data}`);
});
pythonProcess.on("close", (code) => {
  console.log(`child process exited with code ${code}`);
});

/**
 * @param {vscode.ExtensionContext} context
 */

function activate(context) {
  console.log('Congratulations, your extension "varhandler" is now active!');
  let disposable = vscode.commands.registerCommand(
    "varhandler.varChanger",
    function (uri) {
      socket.on("connect", async () => {
        if (uri) {
            const filePath = uri.fsPath;

            if(filePath.endsWith(".c") || filePath.endsWith('.cpp') || filePath.endsWith('.py')) {
              fs.readFile(filePath, (err, data) => {
                if (err) throw err;
                let fileContent = data.toString();
                socket.emit("send_variable", { "fileContent" : fileContent, "filePath" : filePath });
              });
              socket.on("result",async (result) => {
                if(filePath == result['globFilePath']) {
                  fs.writeFile(filePath, result['contents'], (err) => {
                    if (err) {
                      console.error(err);
                      return;
                    }
                  });
                  await vscode.commands.executeCommand('workbench.action.reloadWindow');
                }
              });
            }
            else {
              await vscode.window.showInformationMessage("Only supported for C, C++ and Python files!");
              setTimeout( async () => {
                await vscode.commands.executeCommand('workbench.action.reloadWindow');
              }, 2000)
              await vscode.commands.executeCommand('workbench.action.reloadWindow');
            }
          }
          else {
            await vscode.commands.executeCommand('workbench.action.reloadWindow');
          }
      });
    }
  );

  vscode.window.showInformationMessage("Please wait till the window reloads!");
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
