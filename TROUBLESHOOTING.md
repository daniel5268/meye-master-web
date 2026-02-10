# 🔧 Troubleshooting - Login No Hace POST

## 🐛 Problema Resuelto

El problema era que el formulario estaba haciendo un submit HTML tradicional (GET con query params) en lugar de ejecutar el JavaScript que hace el POST.

### ✅ Soluciones Implementadas:

1. **Prevención de submit por defecto:**
   ```javascript
   form.addEventListener('submit', (e) => {
       e.preventDefault();
       return false;
   });
   ```

2. **Botón con type="button":**
   ```html
   <button type="button" class="btn-submit" id="submitBtn">
   ```

3. **Doble prevención en el click:**
   ```javascript
   submitBtn.addEventListener('click', async (e) => {
       e.preventDefault();
       e.stopPropagation();
       // ... resto del código
   });
   ```

## 🧪 Cómo Verificar que Funciona

### Opción 1: Usar la página de test

1. Abre `test-api.html` en tu navegador:
   ```
   http://localhost:3500/test-api.html
   ```

2. La página automáticamente:
   - ✅ Testea la conexión al backend
   - ✅ Muestra el endpoint exacto
   - ✅ Permite hacer login y ver el request/response
   - ✅ Decodifica el token JWT
   - ✅ Prueba el endpoint de campaigns

3. Ingresa tus credenciales y haz clic en "Test Login"

4. Deberías ver:
   ```
   ✅ LOGIN EXITOSO!
   
   📥 RESPONSE:
   Status: 200
   
   🎫 Token recibido:
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   
   🔓 Claims decodificados:
   {
     "user_id": "uuid-aqui",
     "username": "master",
     "role": "master",
     "exp": 1234567890,
     "iat": 1234567890
   }
   ```

### Opción 2: DevTools del Navegador

1. Abre `http://localhost:3500/login.html`

2. Abre DevTools (F12)

3. Ve a la pestaña **Network**

4. Ingresa credenciales y haz clic en "Iniciar Sesión"

5. Deberías ver un request:
   - **Name:** `login`
   - **Method:** `POST` (no GET)
   - **Status:** `200` (si las credenciales son correctas)
   - **Type:** `xhr` o `fetch`

6. Haz clic en el request y ve a:
   - **Headers:** Verifica `Content-Type: application/json`
   - **Payload:** Verifica `{"username":"master","password":"..."}` (no query params)
   - **Response:** Verifica que tenga `{"token":"..."}`

### Opción 3: Console del Navegador

1. Abre `http://localhost:3500/login.html`

2. Abre la consola (F12 > Console)

3. Pega este código para verificar los event listeners:
   ```javascript
   console.log('Form:', document.getElementById('loginForm'));
   console.log('Submit button:', document.getElementById('submitBtn'));
   console.log('API URL:', window.ENV?.API_BASE_URL || 'http://localhost:3000');
   ```

4. Haz login y verifica que NO veas errores en la consola

## 🔍 Diagnóstico de Problemas Comunes

### Problema 1: Sigue haciendo GET con query params

**Síntomas:**
- URL cambia a `login.html?username=xxx&password=yyy`
- No aparece request POST en Network tab
- Página se recarga

**Causa:** JavaScript no se está ejecutando

**Soluciones:**

1. **Verifica que config.js esté cargado ANTES del HTML:**
   ```html
   <!-- Debe estar ANTES de login.html -->
   <script src="config.js"></script>
   ```

2. **Verifica errores en la consola:**
   - Abre DevTools (F12)
   - Ve a Console
   - Busca errores en rojo
   - Si hay errores de sintaxis, el JavaScript no se ejecuta

3. **Verifica que el script esté dentro del <body>:**
   - El `<script>` debe estar al final del HTML
   - ANTES del cierre `</body>`

4. **Fuerza recarga sin caché:**
   - Chrome/Edge: `Ctrl + Shift + R`
   - Firefox: `Ctrl + F5`
   - O abre en ventana incógnita

### Problema 2: Error de CORS

**Síntomas:**
```
Access to fetch at 'http://localhost:3000/api/v1/users/login' 
from origin 'http://localhost:3500' has been blocked by CORS policy
```

**Solución:** Habilita CORS en tu backend

**Para Express.js:**
```javascript
const cors = require('cors');

app.use(cors({
    origin: 'http://localhost:3500',
    credentials: true,
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));
```

**Para Go (Gin):**
```go
router.Use(cors.New(cors.Config{
    AllowOrigins:     []string{"http://localhost:3500"},
    AllowMethods:     []string{"GET", "POST", "OPTIONS"},
    AllowHeaders:     []string{"Content-Type", "Authorization"},
    AllowCredentials: true,
}))
```

### Problema 3: Request POST se envía pero no llega al backend

**Diagnóstico:**

1. **Verifica la URL en config.js:**
   ```javascript
   window.ENV = {
       API_BASE_URL: 'http://localhost:3000'  // Sin barra al final
   };
   ```

2. **Verifica que el backend esté corriendo:**
   ```bash
   curl -X POST http://localhost:3000/api/v1/users/login \
     -H "Content-Type: application/json" \
     -d '{"username":"master","password":"HolaMundo1991*"}'
   ```

3. **Verifica los logs del backend:**
   - Deberías ver el request POST llegando
   - Si no ves nada, el backend no está recibiendo

### Problema 4: Token no se guarda o no redirige

**Diagnóstico:**

1. **Verifica localStorage:**
   - Abre DevTools (F12)
   - Ve a Application > Local Storage
   - Busca `authToken`

2. **Verifica el token en la consola:**
   ```javascript
   const token = localStorage.getItem('authToken');
   console.log('Token:', token);
   
   // Decodificar
   const parts = token.split('.');
   const payload = JSON.parse(atob(parts[1]));
   console.log('Claims:', payload);
   console.log('Role:', payload.role);
   ```

3. **Verifica que el role sea exactamente "master":**
   - Debe ser lowercase
   - Sin espacios
   - Compara: `payload.role === 'master'`

## 📊 Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Backend está corriendo en `localhost:3000`
- [ ] CORS está habilitado en el backend
- [ ] `config.js` tiene la URL correcta
- [ ] Página se carga sin errores en la consola
- [ ] Network tab muestra request POST (no GET)
- [ ] Request tiene `Content-Type: application/json`
- [ ] Request body es JSON (no query params)
- [ ] Response tiene status 200 y token
- [ ] Token se guarda en localStorage
- [ ] Token tiene claim `role: "master"`
- [ ] Redirección funciona después de login

## 🎯 Test Rápido con cURL

Para verificar que tu backend funciona correctamente:

```bash
# Test login
curl -v -X POST http://localhost:3000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"master","password":"HolaMundo1991*"}'

# Deberías ver:
# < HTTP/1.1 200 OK
# < Content-Type: application/json
# {"token":"eyJhbG..."}

# Guarda el token
TOKEN="eyJhbG..." # Pega el token aquí

# Test campaigns
curl -v -X GET http://localhost:3000/api/v1/campaigns \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# Deberías ver:
# < HTTP/1.1 200 OK
# [{"id":"...","master_id":"...","name":"..."}]
```

## 🔑 Estructura Esperada del JWT

Tu token JWT debe tener esta estructura:

```json
{
  "user_id": "9a984b20-200d-485a-9d3d-83ab9e9e85a6",
  "username": "master",
  "role": "master",
  "exp": 1739141234,
  "iat": 1739137634
}
```

**Importante:**
- `role` debe ser exactamente `"master"` (lowercase)
- `user_id` debe ser un UUID válido
- `exp` debe ser una fecha futura (timestamp Unix)

## 🚀 Si Todo Funciona

Deberías ver este flujo:

1. ✅ Usuario ingresa `username: master`, `password: HolaMundo1991*`
2. ✅ Click en "Iniciar Sesión"
3. ✅ POST request a `http://localhost:3000/api/v1/users/login`
4. ✅ Response 200 con token JWT
5. ✅ Token guardado en localStorage
6. ✅ Token decodificado, role = "master"
7. ✅ Mensaje "¡Inicio de sesión exitoso!"
8. ✅ Redirección a `/dashboard.html` después de 1.5 segundos
9. ✅ Dashboard verifica token y role
10. ✅ GET request a `http://localhost:3000/api/v1/campaigns`
11. ✅ Lista de campañas mostrada

---

**¿Aún tienes problemas?**

1. Usa `test-api.html` para diagnosticar exactamente dónde falla
2. Revisa los logs del backend
3. Verifica la consola del navegador
4. Comparte los errores específicos que ves
