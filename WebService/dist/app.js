"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const dotenv_1 = __importDefault(require("dotenv"));
// Carga las variables de entorno del archivo .env
dotenv_1.default.config();
const app = (0, express_1.default)();
const port = process.env.PORT || 3000;
app.get('/', (req, res) => {
    res.send('¡El servidor del PMS con TypeScript está funcionando!');
});
app.listen(port, () => {
    console.log(`⚡️ [server]: Servidor corriendo en http://localhost:${port}`);
});
