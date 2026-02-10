# Sistema de Autenticación y Dashboard de Maestro

Sistema completo de login con redirección basada en roles y dashboard para maestros de juego.

## 📋 Archivos del Sistema

```
├── login.html          # Página de inicio de sesión
├── dashboard.html      # Dashboard para maestros (role: master)
├── config.js          # Configuración de API URL
├── .env.example       # Ejemplo de variables de entorno
└── README.md          # Esta documentación
```

## 🔄 Flujo de Autenticación

### 1. Login (`login.html`)
- Usuario ingresa credenciales (username + password)
- Validación de formato en frontend
- Request POST a `/api/v1/users/login`
- Si exitoso: 
  - Token JWT guardado en `localStorage`
  - Token decodificado para leer el claim `role`
  - Redirección basada en rol:
    - `role: "master"` → `/dashboard.html`
    - Otros roles → `/player-dashboard.html`

### 2. Dashboard de Maestro (`dashboard.html`)
- Verifica token JWT en `localStorage`
- Decodifica token y valida claim `role === "master"`
- Si no es master o no hay token → Redirige a `/login.html`
- Request GET a `/api/v1/campaigns` con token en header
- Muestra lista de campañas del maestro

## 🔐 Claims del JWT

El token JWT debe contener estos claims:

```json
{
  "user_id": "9a984b20-200d-485a-9d3d-83ab9e9e85a6",
  "username": "johndoe",
  "role": "master",
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Importante:** El claim `role` determina la redirección después del login.

## 🚀 Configuración

### Opción 1: Sin Build Tool

1. **Edita `config.js`:**
   ```javascript
   window.ENV = {
       API_BASE_URL: 'http://localhost:3000'
   };
   ```

2. **Incluye el script en tus HTML:**
   ```html
   <script src="config.js"></script>
   ```

3. **Abre los archivos en el navegador**

### Opción 2: Con Vite/Webpack

1. **Crea `.env`:**
   ```env
   VITE_API_BASE_URL=http://localhost:3000
   ```

2. **Ejecuta tu build tool:**
   ```bash
   npm run dev
   ```

## 📡 API Endpoints Utilizados

### Login
```
POST /api/v1/users/login
```

**Request:**
```json
{
    "username": "johndoe",
    "password": "SecureP@ssw0rd"
}
```

**Response (200):**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Listar Campañas (Solo Masters)
```
GET /api/v1/campaigns
Authorization: Bearer <token>
```

**Response (200):**
```json
[
    {
        "id": "659a49bc-b6c1-4ab4-a763-33d382014174",
        "master_id": "9a984b20-200d-485a-9d3d-83ab9e9e85a6",
        "name": "Dragon's Quest"
    },
    {
        "id": "750e8400-e29b-41d4-a716-446655440001",
        "master_id": "9a984b20-200d-485a-9d3d-83ab9e9e85a6",
        "name": "The Lost Kingdom"
    }
]
```

**Response (403):** Si el usuario no tiene rol de master
```json
{
    "error": "Insufficient permissions (requires Master role)",
    "code": "FORBIDDEN"
}
```

## 🎯 Características del Dashboard

### Estados de la UI

1. **Loading State** 🔄
   - Spinner animado mientras carga
   - Mensaje "Cargando campañas..."

2. **Empty State** 📭
   - Cuando no hay campañas
   - Botón para crear primera campaña
   - Mensaje motivacional

3. **Error State** ⚠️
   - Cuando falla la carga
   - Mensaje de error específico
   - Botón "Reintentar"

4. **Success State** ✅
   - Grid responsive de campañas
   - Cards con información de cada campaña
   - Contador de campañas activas
   - Botón para crear nueva campaña

### Campaign Cards

Cada card muestra:
- 🏰 **Icono de campaña**
- **ID** (primeros 8 caracteres)
- **Nombre** de la campaña
- **Metadata:** Rol de master, estado activo
- **Acciones:** Ver Detalles, Editar

## 🔒 Seguridad

### Protección de Rutas

El dashboard implementa verificaciones de seguridad:

1. **Token Presente:** Verifica que existe token en localStorage
2. **Token Válido:** Intenta decodificar el JWT
3. **Role Check:** Valida que `role === "master"`
4. **Token Expiration:** Redirige a login si el API retorna 401

### Manejo de Tokens

```javascript
// Guardar token
localStorage.setItem('authToken', token);

// Leer token
const token = localStorage.getItem('authToken');

// Usar token en requests
fetch(url, {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});

// Eliminar token (logout)
localStorage.removeItem('authToken');
```

## 🎨 Personalización

### Colores del Dashboard

```css
:root {
    --primary: #0a0e27;      /* Fondo principal */
    --accent: #00ff88;       /* Color de acento */
    --text: #e8edf5;         /* Texto principal */
    --text-dim: #8b95a8;     /* Texto secundario */
    --surface: #141829;      /* Fondo de cards */
    --border: rgba(0, 255, 136, 0.15); /* Bordes */
}
```

### Cambiar URLs de Navegación

**En dashboard.html:**

```javascript
// Ver detalles de campaña
function viewCampaign(campaignId) {
    window.location.href = `/campaign-detail.html?id=${campaignId}`;
}

// Editar campaña
function editCampaign(campaignId) {
    window.location.href = `/campaign-edit.html?id=${campaignId}`;
}
```

## 🐛 Troubleshooting

### El usuario no ve el dashboard después del login

**Posibles causas:**
1. El JWT no contiene el claim `role: "master"`
2. El token no se está guardando correctamente
3. La URL de redirección es incorrecta

**Solución:**
- Abre la consola del navegador (F12)
- Ve a Application → Local Storage
- Verifica que `authToken` existe
- Copia el token y decodifícalo en [jwt.io](https://jwt.io)
- Verifica que el claim `role` sea `"master"`

### Error 403 al cargar campañas

**Causa:** El usuario no tiene rol de master

**Solución:**
- Verifica que el backend asigne correctamente el rol
- El claim `role` en el JWT debe ser exactamente `"master"` (lowercase)

### Error de CORS

**Solución:**
```javascript
// En tu backend (Express.js)
app.use(cors({
    origin: 'http://localhost:5173',
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### Campañas no se muestran

**Verifica:**
1. URL del API es correcta en config.js
2. Backend está corriendo
3. Endpoint `/api/v1/campaigns` está implementado
4. Token se envía en header Authorization
5. Revisa la consola del navegador para errores

## 📱 Responsive Design

El dashboard es completamente responsive:
- **Desktop:** Grid de 3-4 columnas
- **Tablet:** Grid de 2 columnas
- **Mobile:** Lista vertical (1 columna)

## 🔄 Próximos Pasos

Páginas sugeridas para implementar:
- [ ] `player-dashboard.html` - Dashboard para jugadores
- [ ] `campaign-detail.html` - Ver detalles de una campaña
- [ ] `campaign-edit.html` - Editar campaña
- [ ] `campaign-create.html` - Crear nueva campaña

## 📚 Estructura de Datos

### CampaignSummary (API Response)
```typescript
interface CampaignSummary {
    id: string;           // UUID de la campaña
    master_id: string;    // UUID del maestro
    name: string;         // Nombre de la campaña
}
```

### JWT Claims
```typescript
interface JWTClaims {
    user_id: string;      // UUID del usuario
    username: string;     // Nombre de usuario
    role: string;         // "master" | "player" | otros
    exp: number;          // Timestamp de expiración
    iat: number;          // Timestamp de emisión
}
```

## 🎮 Flujo Completo de Usuario

```
1. Usuario abre login.html
   ↓
2. Ingresa username y password
   ↓
3. POST /api/v1/users/login
   ↓
4. Token JWT retornado
   ↓
5. Token decodificado → role === "master"
   ↓
6. Redirige a dashboard.html
   ↓
7. Dashboard verifica token y rol
   ↓
8. GET /api/v1/campaigns con Bearer token
   ↓
9. Lista de campañas mostrada
   ↓
10. Usuario puede:
    - Ver detalles de campaña
    - Editar campaña
    - Crear nueva campaña
    - Cerrar sesión
```

## ⚡ Performance

- Animaciones optimizadas con CSS
- Lazy loading de imágenes
- Debouncing en validaciones
- Carga asíncrona de datos
- Estados de loading visuales

## 🎯 Best Practices Implementadas

✅ Validación de inputs en cliente y servidor
✅ Manejo robusto de errores
✅ Estados de UI claros (loading, error, empty, success)
✅ Responsive design mobile-first
✅ Seguridad con JWT y role-based access
✅ UX fluida con animaciones
✅ Feedback visual inmediato
✅ Código limpio y comentado

---

**Versión:** 1.0  
**Última actualización:** 2026-02-09
