// =========================
//   VERIFICAR AUTENTICACIÓN
// =========================
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = '/login';
}

const authHeaders = {
    'Authorization': `Bearer ${token}`
};

// =========================
//   VARIABLES GLOBALES
// =========================
let currentEditId = null;

// =========================
//   TABS
// =========================
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

        btn.classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');

        if (tabName === 'products') loadProducts();
        if (tabName === 'config') loadConfig();
    });
});

// =========================
//   LOGOUT
// =========================
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
});

// =========================
//   CARGAR PRODUCTOS
// =========================
async function loadProducts() {
    try {
        const response = await fetch('/api/products', {
            headers: authHeaders
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            return;
        }

        const products = await response.json();
        const productsList = document.getElementById('productsList');

        if (products.length === 0) {
            productsList.innerHTML = '<p class="no-products">No hay productos. Agrega el primero.</p>';
            return;
        }

        productsList.innerHTML = products.map(p => `
            <div class="product-item">
                <img src="data:image/jpeg;base64,${p.image}" alt="${p.name}">
                <div class="product-item-info">
                    <h4>${p.name}</h4>
                    ${p.description ? `<p>${p.description}</p>` : ''}
                    ${p.price ? `<p><strong>$${p.price.toFixed(2)}</strong></p>` : ''}
                </div>
                <div class="product-item-actions">
                    <button class="btn-edit" onclick="editProduct(${p.id})">Editar</button>
                    <button class="btn-delete" onclick="deleteProduct(${p.id})">Eliminar</button>
                </div>
            </div>
        `).join('');

    } catch (error) {
        showMessage('Error al cargar productos', 'error');
    }
}

// =========================
//   MODAL PRODUCTOS
// =========================
const modal = document.getElementById('productModal');
const addBtn = document.getElementById('addProductBtn');
const closeBtn = document.querySelector('.close');

addBtn.onclick = () => {
    currentEditId = null;
    document.getElementById('modalTitle').textContent = 'Agregar Producto';
    document.getElementById('productForm').reset();
    document.getElementById('productId').value = '';
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('productImage').required = true;
    modal.classList.add('active');
};

closeBtn.onclick = closeProductModal;

window.onclick = (e) => {
    if (e.target === modal) closeProductModal();
};

function closeProductModal() {
    modal.classList.remove('active');
}

// =========================
//   PREVIEW IMAGEN
// =========================
document.getElementById('productImage').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('imagePreview');
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

// =========================
//   GUARDAR PRODUCTO
// =========================
document.getElementById('productForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('name', document.getElementById('productName').value);
    formData.append('description', document.getElementById('productDescription').value);
    formData.append('price', document.getElementById('productPrice').value || '');

    const imageFile = document.getElementById('productImage').files[0];
    if (imageFile) formData.append('image', imageFile);

    try {
        let url = '/api/products';
        let method = 'POST';

        if (currentEditId) {
            url = `/api/products/${currentEditId}`;
            method = 'PUT';
        }

        const response = await fetch(url, {
            method,
            headers: authHeaders,
            body: formData
        });

        if (response.ok) {
            showMessage('Producto guardado exitosamente', 'success');
            closeProductModal();
            loadProducts();
        } else {
            const data = await response.json();
            showMessage(data.detail || 'Error al guardar producto', 'error');
        }
    } catch (error) {
        showMessage('Error de conexión', 'error');
    }
});

// =========================
//   EDITAR PRODUCTO
// =========================
async function editProduct(id) {
    try {
        const response = await fetch('/api/products', {
            headers: authHeaders
        });
        const products = await response.json();
        const product = products.find(p => p.id === id);

        if (product) {
            currentEditId = id;
            document.getElementById('modalTitle').textContent = 'Editar Producto';
            document.getElementById('productId').value = id;
            document.getElementById('productName').value = product.name;
            document.getElementById('productDescription').value = product.description || '';
            document.getElementById('productPrice').value = product.price || '';
            document.getElementById('productImage').required = false;

            if (product.image) {
                const preview = document.getElementById('imagePreview');
                preview.src = `data:image/jpeg;base64,${product.image}`;
                preview.style.display = 'block';
            }

            modal.classList.add('active');
        }
    } catch (error) {
        showMessage('Error al cargar producto', 'error');
    }
}

// =========================
//   ELIMINAR PRODUCTO
// =========================
async function deleteProduct(id) {
    if (!confirm('¿Estás seguro de eliminar este producto?')) return;

    try {
        const response = await fetch(`/api/products/${id}`, {
            method: 'DELETE',
            headers: authHeaders
        });

        if (response.ok) {
            showMessage('Producto eliminado exitosamente', 'success');
            loadProducts();
        } else {
            showMessage('Error al eliminar producto', 'error');
        }
    } catch (error) {
        showMessage('Error de conexión', 'error');
    }
}

// =========================
//   CARGAR CONFIGURACIÓN
// =========================
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();

        document.getElementById('primaryColor').value = config.primary_color;
        document.getElementById('backgroundColor').value = config.background_color;
        document.getElementById('productBgColor').value = config.product_bg_color;

        // ⭐ NUEVO: WhatsApp
        document.getElementById('whatsappNumber').value = config.whatsapp_number || '';

    } catch (error) {
        showMessage('Error al cargar configuración', 'error');
    }
}

// =========================
//   GUARDAR CONFIGURACIÓN
// =========================
document.getElementById('configForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const config = {
        primary_color: document.getElementById('primaryColor').value,
        background_color: document.getElementById('backgroundColor').value,
        product_bg_color: document.getElementById('productBgColor').value,
        
        // ⭐ NUEVO
        whatsapp_number: document.getElementById('whatsappNumber').value
    };

    try {
        const response = await fetch('/api/config', {
            method: 'PUT',
            headers: {
                ...authHeaders,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });

        if (response.ok) {
            showMessage('Configuración guardada exitosamente', 'success');
        } else {
            showMessage('Error al guardar configuración', 'error');
        }
    } catch (error) {
        showMessage('Error de conexión', 'error');
    }
});

// =========================
//   NOTIFICACIONES
// =========================
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;

    setTimeout(() => {
        messageDiv.className = 'message';
    }, 4000);
}

// =========================
//   INICIALIZAR
// =========================
loadProducts();
