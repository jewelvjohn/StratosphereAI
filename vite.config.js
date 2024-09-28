import {defineConfig} from 'vite'
import path from 'path'

const root = path.resolve(__dirname, 'src');
const outDir = path.resolve(__dirname, 'dist');

export default defineConfig({
    root: root,
    base: '/stratosphere/',
    build: {
        outDir: outDir,
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: path.resolve(root, 'index.html')
            }
        }
    }
});