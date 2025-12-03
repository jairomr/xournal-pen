# Guia de Teste Local

## 🚀 Teste Rápido

### Passo 1: Instalar

```bash
# Clone o repositório (se ainda não tiver)
git clone https://github.com/jairomr/xournal-pen.git
cd xournal-pen

# Execute o instalador
chmod +x INSTALL.sh
./INSTALL.sh
```

O script vai:
- Criar ambiente virtual Python
- Instalar todas as dependências (PyQt5, pynput, etc)
- Criar script `run.sh` para execução

### Passo 2: Executar

```bash
./run.sh
```

Ou manualmente:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar
python src/main.py
```

### Passo 3: Testar

1. **Abra o Xournal++** em outra janela

2. **Teste com teclado:**
   - Pressione `Alt+R`
   - Menu deve aparecer!
   - Mova o mouse sobre as fatias (deve highlightar)
   - Clique em uma cor ou ferramenta
   - Verificar se mudou no Xournal++

3. **Teste com stylus:**
   - Pressione o botão lateral da caneta
   - Menu deve aparecer na posição da caneta
   - Toque em uma fatia para selecionar

## 🐛 Problemas Comuns

### "ModuleNotFoundError: No module named 'PyQt5'"

**Solução:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied: ./run.sh"

**Solução:**
```bash
chmod +x run.sh
chmod +x INSTALL.sh
```

### Botão da stylus não funciona

**Causa:** Botão não está configurado ou não é detectado

**Teste:**
```bash
# Testar captura de eventos
python src/stylus_handler.py
# Pressione o botão e veja se aparece mensagem
```

**Se não detectar:**
- Use `Alt+R` como alternativa
- Configure botão no driver da tablet
- Veja `STYLUS_CONFIG.md` para instruções detalhadas

### Menu não aparece

**Debug passo a passo:**

1. **Verificar se aplicação está rodando:**
   ```bash
   ps aux | grep python | grep main.py
   ```

2. **Ver mensagens de erro:**
   ```bash
   python src/main.py
   # Veja output no terminal
   ```

3. **Testar componentes individualmente:**

   **Testar handler de stylus:**
   ```bash
   python src/stylus_handler.py
   ```

   **Testar controle do Xournal++:**
   ```bash
   python src/xournal_controller.py
   ```

### "OpenGL version detected: 1.1" (erro antigo do Kivy)

**Resolução:** Esse erro foi resolvido! Agora usamos PyQt5 que não depende de OpenGL.

Se você ainda vê esse erro:
```bash
# Limpar cache do pip
pip cache purge

# Reinstalar
pip uninstall kivy kivymd
pip install -r requirements.txt
```

### Ações não funcionam no Xournal++

**Problema:** Atalhos podem ser diferentes na sua versão

**Solução:** Edite `src/xournal_controller.py`:

```python
self.color_shortcuts = {
    "Preto": "1",  # ← Mude para o atalho que você usa
    "Azul": "2",
    # ...
}
```

**Como descobrir os atalhos:**
1. Abra Xournal++
2. Vá em `Editar → Preferências → Atalhos de Teclado`
3. Anote os atalhos para cores e ferramentas
4. Atualize `xournal_controller.py`

## ✅ Checklist de Teste

Antes de reportar um bug, verifique:

- [ ] Ambiente virtual está ativado (`source venv/bin/activate`)
- [ ] Todas as dependências instaladas (`pip list | grep PyQt5`)
- [ ] Xournal++ está aberto e em foco
- [ ] Testou com `Alt+R` (não só com botão da stylus)
- [ ] Viu mensagens no terminal ao executar
- [ ] Testou componentes individualmente

## 📊 Verificar Versões

```bash
# Ativar venv
source venv/bin/activate

# Verificar versões
python --version          # Deve ser 3.8+
pip show PyQt5           # Deve estar instalado
pip show pynput          # Deve estar instalado
pip show pyautogui       # Deve estar instalado
```

## 🧪 Teste Avançado

### Teste de Performance

```bash
# Ver uso de CPU/memória
python src/main.py &
PID=$!
top -p $PID

# Parar
kill $PID
```

### Teste de Build Local

```bash
# Instalar PyInstaller
pip install pyinstaller

# Build
pyinstaller --onefile --noconsole --name xournal-radial-menu src/main.py

# Testar executável
./dist/xournal-radial-menu
```

## 📝 Reportar Bug

Se encontrar um problema, inclua:

1. **Sistema operacional e versão:**
   ```bash
   uname -a
   python --version
   ```

2. **Versão do Xournal++:**
   ```bash
   xournalpp --version
   ```

3. **Log de erro completo:**
   ```bash
   python src/main.py 2>&1 | tee error.log
   ```

4. **Passos para reproduzir**

5. **Comportamento esperado vs observado**

---

**Dica:** Mantenha o terminal aberto enquanto testa para ver mensagens de debug!
