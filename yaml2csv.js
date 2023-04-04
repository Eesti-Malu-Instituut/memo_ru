const fs = require('fs')
const YAML = require('yaml')
// import fs from 'fs'
// import YAML from 'yaml'

const file = fs.readFileSync('./all_utf8_short.yaml')
YAML.parse(file)