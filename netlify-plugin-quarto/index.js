const { execSync } = require('child_process')

module.exports = {
    onPreBuild: () => {
        console.log("Installing Quarto...")
        execSync('curl -fsSL https://quarto.org/download/latest/quarto-linux-amd64.deb -o quarto.deb && sudo dpkg -i quarto.deb')
    }
}
