# Como Criar uma Release

## ⚠️ Nota sobre Tags

O push de tags pode falhar com erro 403 devido a restrições de permissões.
Se isso acontecer, use a interface web do GitHub.

## 📦 Método 1: Via Interface Web do GitHub (Recomendado)

### Passo 1: Acessar Releases

1. Vá para o repositório no GitHub
2. Clique em **"Releases"** (no menu lateral direito)
3. Clique em **"Draft a new release"** ou **"Create a new release"**

### Passo 2: Criar a Tag

1. Em **"Choose a tag"**, digite: `v2.0.0`
2. Clique em **"Create new tag: v2.0.0 on publish"**
3. Target: Selecione o branch `claude/xournal-radial-menu-plugin-01QW9SnNvsA2onhSZzBBFQi2`

### Passo 3: Preencher Informações da Release

**Release title:** `v2.0.0 - Python Standalone Application`

**Description:**
```markdown
## 🎉 Primeira Release Oficial!

Aplicação Python standalone para menu radial no Xournal++.

### ✨ Funcionalidades

- **Menu radial completo** com 8 cores + 10 ferramentas
- **Captura nativa** de botão lateral da stylus
- **Overlay real** sobre Xournal++ (não desenha na página)
- **Detecção automática** da posição do cursor
- **Hover highlighting** em tempo real
- **Cross-platform**: Linux, Windows, macOS

### 🚀 Melhorias sobre Versão Lua

- ✅ Menu aparece na posição real do cursor
- ✅ Não interfere com o documento
- ✅ Sem erros de API
- ✅ Captura de stylus nativa
- ✅ Muito mais responsivo

### 📥 Como Usar

1. Baixe o executável para seu sistema:
   - **Linux**: `xournal-radial-menu-linux`
   - **Windows**: `xournal-radial-menu-windows.exe`
   - **macOS**: `xournal-radial-menu-macos`

2. Torne executável (Linux/macOS):
   ```bash
   chmod +x xournal-radial-menu-linux
   ```

3. Execute:
   ```bash
   ./xournal-radial-menu-linux
   ```

4. Use:
   - Pressione **botão lateral da stylus** ou **Alt+R**
   - Menu aparece!
   - Mova e toque para selecionar

### 📋 Instalação do Código-Fonte

```bash
git clone https://github.com/jairomr/xournal-pen.git
cd xournal-pen
./INSTALL.sh
./run.sh
```

### 📖 Documentação Completa

Veja [README.md](README.md) e [CHANGELOG.md](CHANGELOG.md)

---

**Nota**: Os executáveis serão gerados automaticamente pelo GitHub Actions após a criação desta release.
```

### Passo 4: Publicar

1. **NÃO marque** "This is a pre-release"
2. **Marque** "Set as the latest release"
3. Clique em **"Publish release"**

### Passo 5: Aguardar Build

O GitHub Actions vai:
1. Detectar a tag `v2.0.0`
2. Buildar executáveis para Linux, Windows e macOS
3. Anexar os executáveis automaticamente à release

Acompanhe em: **Actions** → **Build and Release**

---

## 🛠️ Método 2: Trigger Manual do Build

Se você quiser apenas testar o build sem criar release:

1. Vá para **Actions**
2. Selecione **"Build and Release"** no menu lateral
3. Clique em **"Run workflow"**
4. Selecione o branch desejado
5. Clique em **"Run workflow"**

Os artifacts estarão disponíveis no workflow concluído.

---

## 🔧 Método 3: Via Git (Se Permissões Permitirem)

```bash
# Criar tag anotada
git tag -a v2.0.0 -m "Release v2.0.0 - Python Standalone Application"

# Push da tag
git push origin v2.0.0
# OU
git push --tags
```

---

## 📝 Checklist de Release

Antes de criar a release, verifique:

- [ ] Código no branch correto (claude/xournal-radial-menu-plugin-01QW9SnNvsA2onhSZzBBFQi2)
- [ ] CHANGELOG.md atualizado
- [ ] README.md atualizado com versão correta
- [ ] Todos os testes passando
- [ ] Workflow de build configurado corretamente
- [ ] Versão no pyproject.toml atualizada (2.0.0)

---

## 🐛 Troubleshooting

### Build Falha

1. Vá em **Actions** → workflow que falhou
2. Clique no job que falhou (build-linux, build-windows, build-macos)
3. Veja os logs para identificar o erro
4. Corrija o erro e faça novo commit
5. Crie nova tag (v2.0.1, por exemplo)

### Executáveis Não Anexados

Se a release for criada mas os executáveis não aparecerem:

1. Vá em **Actions** → último workflow "Build and Release"
2. Verifique se todos os jobs completaram com sucesso
3. Baixe os artifacts manualmente se necessário
4. Edite a release e anexe os arquivos manualmente

---

## 🎯 Versões Futuras

Para criar versões futuras (v2.0.1, v2.1.0, etc):

1. Atualize o código
2. Atualize CHANGELOG.md
3. Atualize pyproject.toml (versão)
4. Commit e push
5. Crie nova release seguindo os passos acima

---

**Boa sorte com a release! 🚀**
