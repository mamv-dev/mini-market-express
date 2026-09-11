import streamlit as st
from datetime import datetime

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Mini Market Express",
    page_icon="🛒",
    layout="wide"
)

# ============================================================
# CAPA DE DATOS - Simula BD relacional (productos, ventas, detalle_ventas)
# ============================================================
if "productos" not in st.session_state:
    st.session_state.productos = [
        {"id": 1, "codigo": "P001", "nombre": "Café expreso", "stock": 50,
         "precio_compra": 0.80, "precio_venta": 1.50, "stock_minimo": 10},
        {"id": 2, "codigo": "P002", "nombre": "Pan de jamón", "stock": 30,
         "precio_compra": 1.80, "precio_venta": 2.80, "stock_minimo": 8},
        {"id": 3, "codigo": "P003", "nombre": "Refresco 350ml", "stock": 60,
         "precio_compra": 0.60, "precio_venta": 1.20, "stock_minimo": 15},
        {"id": 4, "codigo": "P004", "nombre": "Chocolates", "stock": 40,
         "precio_compra": 0.45, "precio_venta": 0.90, "stock_minimo": 12},
        {"id": 5, "codigo": "P005", "nombre": "Agua mineral 500ml", "stock": 80,
         "precio_compra": 0.35, "precio_venta": 0.75, "stock_minimo": 20},
        {"id": 6, "codigo": "P006", "nombre": "Papas fritas", "stock": 25,
         "precio_compra": 0.55, "precio_venta": 1.10, "stock_minimo": 10},
        {"id": 7, "codigo": "P007", "nombre": "Galletas", "stock": 45,
         "precio_compra": 0.30, "precio_venta": 0.60, "stock_minimo": 15},
        {"id": 8, "codigo": "P008", "nombre": "Jugo natural", "stock": 20,
         "precio_compra": 1.20, "precio_venta": 2.00, "stock_minimo": 8},
        {"id": 9, "codigo": "P009", "nombre": "Sándwich", "stock": 15,
         "precio_compra": 2.00, "precio_venta": 3.50, "stock_minimo": 5},
        {"id": 10, "codigo": "P010", "nombre": "Helado", "stock": 18,
         "precio_compra": 1.00, "precio_venta": 1.80, "stock_minimo": 6},
    ]

if "ventas" not in st.session_state:
    st.session_state.ventas = []

if "detalle_ventas" not in st.session_state:
    st.session_state.detalle_ventas = []

if "contador_producto" not in st.session_state:
    st.session_state.contador_producto = 11

if "contador_venta" not in st.session_state:
    st.session_state.contador_venta = 1

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "ultima_venta" not in st.session_state:
    st.session_state.ultima_venta = None


# ============================================================
# FUNCIONES DE DATOS (Capa de Datos)
# ============================================================
def obtener_productos():
    return st.session_state.productos


def obtener_producto_por_id(id_producto):
    for p in st.session_state.productos:
        if p["id"] == id_producto:
            return p
    return None


def obtener_producto_por_codigo(codigo):
    for p in st.session_state.productos:
        if p["codigo"] == codigo:
            return p
    return None


def agregar_producto(codigo, nombre, stock, precio_compra, precio_venta, stock_minimo):
    if obtener_producto_por_codigo(codigo):
        return False, f"❌ Ya existe un producto con el código {codigo}"
    nuevo = {
        "id": st.session_state.contador_producto,
        "codigo": codigo,
        "nombre": nombre,
        "stock": stock,
        "precio_compra": precio_compra,
        "precio_venta": precio_venta,
        "stock_minimo": stock_minimo
    }
    st.session_state.productos.append(nuevo)
    st.session_state.contador_producto += 1
    return True, f"✅ Producto '{nombre}' agregado correctamente"


def modificar_producto(id_producto, codigo, nombre, stock, precio_compra, precio_venta, stock_minimo):
    p = obtener_producto_por_id(id_producto)
    if not p:
        return False, "❌ Producto no encontrado"
    existente = obtener_producto_por_codigo(codigo)
    if existente and existente["id"] != id_producto:
        return False, f"❌ El código {codigo} ya está en uso"
    p["codigo"] = codigo
    p["nombre"] = nombre
    p["stock"] = stock
    p["precio_compra"] = precio_compra
    p["precio_venta"] = precio_venta
    p["stock_minimo"] = stock_minimo
    return True, f"✅ Producto '{nombre}' modificado correctamente"


def eliminar_producto(id_producto):
    p = obtener_producto_por_id(id_producto)
    if not p:
        return False, "❌ Producto no encontrado"
    st.session_state.productos = [prod for prod in st.session_state.productos if prod["id"] != id_producto]
    return True, f"✅ Producto '{p['nombre']}' eliminado correctamente"


def registrar_venta(items):
    if not items:
        return False, "❌ No hay items en la venta", None
    for item in items:
        p = obtener_producto_por_id(item["producto_id"])
        if not p:
            return False, f"❌ Producto no encontrado", None
        if p["stock"] < item["cantidad"]:
            return False, f"❌ Stock insuficiente para '{p['nombre']}' (disponible: {p['stock']})", None
    
    total = 0
    detalles = []
    for item in items:
        p = obtener_producto_por_id(item["producto_id"])
        subtotal = p["precio_venta"] * item["cantidad"]
        total += subtotal
        detalles.append({
            "producto_id": p["id"],
            "codigo": p["codigo"],
            "nombre": p["nombre"],
            "cantidad": item["cantidad"],
            "precio_unitario": p["precio_venta"],
            "subtotal": subtotal
        })
    
    venta = {
        "id": st.session_state.contador_venta,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": total,
        "items": detalles
    }
    st.session_state.ventas.append(venta)
    
    for item in items:
        p = obtener_producto_por_id(item["producto_id"])
        p["stock"] -= item["cantidad"]
    
    for d in detalles:
        st.session_state.detalle_ventas.append({
            "id": len(st.session_state.detalle_ventas) + 1,
            "venta_id": venta["id"],
            **d
        })
    
    st.session_state.contador_venta += 1
    return True, f"✅ Venta #{venta['id']} registrada por ${total:,.2f}", venta


def productos_con_stock_bajo():
    return [p for p in st.session_state.productos if p["stock"] <= p["stock_minimo"]]


def valor_inventario():
    vc = sum(p["stock"] * p["precio_compra"] for p in st.session_state.productos)
    vv = sum(p["stock"] * p["precio_venta"] for p in st.session_state.productos)
    return vc, vv


def total_ventas():
    return sum(v["total"] for v in st.session_state.ventas)


def ganancia_total():
    gan = 0
    for d in st.session_state.detalle_ventas:
        p = obtener_producto_por_id(d["producto_id"])
        if p:
            gan += (d["precio_unitario"] - p["precio_compra"]) * d["cantidad"]
    return gan


def producto_mas_vendido():
    if not st.session_state.detalle_ventas:
        return None, 0
    conteo = {}
    for d in st.session_state.detalle_ventas:
        conteo[d["nombre"]] = conteo.get(d["nombre"], 0) + d["cantidad"]
    if not conteo:
        return None, 0
    nombre = max(conteo, key=conteo.get)
    return nombre, conteo[nombre]


# ============================================================
# CAPA DE IA - Asistente inteligente
# ============================================================
def responder_consulta(pregunta):
    pregunta = pregunta.lower()
    
    if "stock bajo" in pregunta or "reponer" in pregunta or "agotado" in pregunta:
        bajos = productos_con_stock_bajo()
        if not bajos:
            return "✅ No hay productos con stock bajo. Todo está en orden."
        respuesta = "⚠️ **Productos con stock bajo que necesitan reposición:**\n\n"
        for p in bajos:
            respuesta += f"- **{p['nombre']}** ({p['codigo']}): {p['stock']} uds (mínimo: {p['stock_minimo']})\n"
        return respuesta
    
    if "venta" in pregunta and ("total" in pregunta or "cuánto" in pregunta or "cuanto" in pregunta):
        return f"💰 El total de ventas es **${total_ventas():,.2f}**"
    
    if "ganancia" in pregunta or "utilidad" in pregunta:
        return f"📈 La ganancia total es **${ganancia_total():,.2f}**"
    
    if "más vendido" in pregunta or "mas vendido" in pregunta or "top" in pregunta:
        nombre, cant = producto_mas_vendido()
        if not nombre:
            return "ℹ️ Aún no hay ventas registradas."
        return f"🏆 El producto más vendido es **{nombre}** con **{cant} unidades**"
    
    if "inventario" in pregunta or "valor" in pregunta:
        vc, vv = valor_inventario()
        return (f"💼 **Valor del inventario:**\n"
                f"- Compra: **${vc:,.2f}**\n"
                f"- Venta: **${vv:,.2f}**\n"
                f"- Ganancia potencial: **${vv-vc:,.2f}**")
    
    if "cuántos productos" in pregunta or "cuantos productos" in pregunta:
        return f"📦 Hay **{len(obtener_productos())} productos** registrados."
    
    if "sugerencia" in pregunta or "recomendación" in pregunta or "recomendacion" in pregunta:
        sugerencias = ["🧠 **Sugerencias:**\n"]
        bajos = productos_con_stock_bajo()
        if bajos:
            sugerencias.append(f"⚠️ Reponer {len(bajos)} productos con stock bajo")
        else:
            sugerencias.append("✅ Stock saludable")
        prods = obtener_productos()
        if prods:
            margenes = [(p["nombre"], (p["precio_venta"]-p["precio_compra"])/p["precio_compra"]*100) for p in prods]
            margenes.sort(key=lambda x: x[1], reverse=True)
            sugerencias.append(f"💎 Mejor margen: {margenes[0][0]} ({margenes[0][1]:.1f}%)")
            sugerencias.append(f"📉 Menor margen: {margenes[-1][0]} ({margenes[-1][1]:.1f}%)")
        if st.session_state.ventas:
            sugerencias.append(f"📈 Ganancia acumulada: ${ganancia_total():,.2f}")
        return "\n".join(sugerencias)
    
    return ("🤖 No entendí. Prueba:\n"
            "- '¿Qué productos tienen stock bajo?'\n"
            "- '¿Cuál es el total de ventas?'\n"
            "- '¿Cuál es la ganancia?'\n"
            "- '¿Cuál es el producto más vendido?'\n"
            "- '¿Cuánto vale el inventario?'\n"
            "- 'Dame sugerencias'")


# ============================================================
# FUNCIONES AUXILIARES GUI
# ============================================================
def badge_stock(stock, stock_minimo):
    if stock == 0:
        return "🔴 AGOTADO"
    elif stock <= stock_minimo:
        return "🟡 STOCK BAJO"
    elif stock <= stock_minimo * 1.5:
        return "🟠 MODERADO"
    return "🟢 OK"


def barra_stock(stock, stock_minimo, stock_max=100):
    porcentaje = min(100, (stock / stock_max) * 100)
    if stock == 0:
        color = "#f44336"
    elif stock <= stock_minimo:
        color = "#ff9800"
    elif stock <= stock_minimo * 1.5:
        color = "#ffc107"
    else:
        color = "#4caf50"
    return (f'<div style="background-color:#e0e0e0;border-radius:5px;height:20px;width:100%;margin:3px 0;">'
            f'<div style="background-color:{color};border-radius:5px;height:20px;width:{porcentaje}%;'
            f'display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:bold;">'
            f'{stock}</div></div>')


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================
st.title("🛒 Mini Market Express")
st.markdown("""
**Módulos disponibles:**
- 📦 Gestión de productos (Alta, Baja, Modificación)
- 💰 Punto de venta (generación de tickets)
- ⚠️ Alertas de stock bajo
- 📊 Reportes y análisis
- 🤖 Asistente IA
""")
st.markdown("---")

# Sidebar - Navegación
st.sidebar.title("🛒 Mini Market Express")
st.sidebar.markdown("### 🧭 Navegación")
seccion = st.sidebar.radio(
    "Selecciona un módulo:",
    ["🏠 Inicio", "📦 Productos", "💰 Punto de Venta", "📊 Reportes", "🤖 Asistente IA"]
)

# Alerta global en sidebar
bajos = productos_con_stock_bajo()
if bajos:
    st.sidebar.markdown("---")
    st.sidebar.error(f"⚠️ **{len(bajos)} producto(s) con stock bajo**")
    for p in bajos[:5]:
        st.sidebar.caption(f"• {p['nombre']} ({p['stock']} uds)")


# ============================================================
# SECCIÓN: INICIO
# ============================================================
if seccion == "🏠 Inicio":
    st.header("🏠 Panel Principal - Mini Market Express")
    
    prods = obtener_productos()
    vc, vv = valor_inventario()
    total_v = total_ventas()
    gan = ganancia_total()
    bajos = productos_con_stock_bajo()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📦 Productos", len(prods))
    col2.metric("💰 Ventas Totales", f"${total_v:,.2f}")
    col3.metric("📈 Ganancia", f"${gan:,.2f}")
    col4.metric("💼 Valor Inventario", f"${vc:,.2f}")
    col5.metric("⚠️ Stock Bajo", len(bajos))
    
    st.markdown("---")
    st.subheader("⚠️ Alertas de Stock")
    if bajos:
        for p in bajos:
            st.warning(f"🔔 **{p['nombre']}** ({p['codigo']}) — Stock: **{p['stock']}** | Mínimo: **{p['stock_minimo']}**")
    else:
        st.success("✅ Todos los productos tienen stock suficiente.")
    
    st.markdown("---")
    st.subheader("📋 Estado del Inventario")
    tabla = "| Código | Producto | Stock | Estado | Precio Venta |\n"
    tabla += "|--------|----------|-------|--------|--------------|\n"
    for p in prods:
        badge = badge_stock(p["stock"], p["stock_minimo"])
        tabla += f"| {p['codigo']} | {p['nombre']} | {p['stock']} | {badge} | ${p['precio_venta']:.2f} |\n"
    st.markdown(tabla)


# ============================================================
# SECCIÓN: PRODUCTOS (CRUD)
# ============================================================
elif seccion == "📦 Productos":
    st.header("📦 Gestión de Productos - Mini Market Express")
    
    tab_lista, tab_alta, tab_mod, tab_baja = st.tabs(["📋 Lista", "➕ Alta", "✏️ Modificar", "🗑️ Baja"])
    
    with tab_lista:
        st.subheader("📋 Lista de Productos")
        prods = obtener_productos()
        if not prods:
            st.info("ℹ️ No hay productos registrados.")
        else:
            for p in prods:
                col1, col2 = st.columns([3, 1])
                with col1:
                    badge = badge_stock(p["stock"], p["stock_minimo"])
                    st.markdown(f"**{p['codigo']}** — {p['nombre']} — {badge}")
                    st.caption(f"Stock: {p['stock']} | Mín: {p['stock_minimo']} | "
                               f"Compra: ${p['precio_compra']:.2f} | Venta: ${p['precio_venta']:.2f}")
                with col2:
                    st.html(barra_stock(p["stock"], p["stock_minimo"]))
                st.markdown("---")
    
    with tab_alta:
        st.subheader("➕ Dar de Alta un Producto")
        with st.form("form_alta"):
            col1, col2 = st.columns(2)
            with col1:
                codigo = st.text_input("Código *", placeholder="Ej: P011")
                nombre = st.text_input("Nombre *", placeholder="Ej: Chicle menta")
                stock = st.number_input("Stock inicial *", min_value=0, value=10)
            with col2:
                precio_compra = st.number_input("Precio compra ($) *", min_value=0.0, value=0.50, step=0.10)
                precio_venta = st.number_input("Precio venta ($) *", min_value=0.0, value=1.00, step=0.10)
                stock_minimo = st.number_input("Stock mínimo *", min_value=0, value=5)
            
            submitted = st.form_submit_button("✅ Agregar Producto")
            if submitted:
                if not codigo or not nombre:
                    st.error("❌ Código y nombre son obligatorios")
                elif precio_venta < precio_compra:
                    st.error("❌ El precio de venta no puede ser menor al de compra")
                else:
                    ok, msg = agregar_producto(codigo, nombre, stock, precio_compra, precio_venta, stock_minimo)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    
    with tab_mod:
        st.subheader("✏️ Modificar Producto")
        prods = obtener_productos()
        if not prods:
            st.info("ℹ️ No hay productos para modificar.")
        else:
            opciones = {f"{p['codigo']} - {p['nombre']}": p for p in prods}
            seleccionado = st.selectbox("Selecciona un producto:", list(opciones.keys()))
            p = opciones[seleccionado]
            with st.form("form_mod"):
                col1, col2 = st.columns(2)
                with col1:
                    codigo = st.text_input("Código", value=p["codigo"])
                    nombre = st.text_input("Nombre", value=p["nombre"])
                    stock = st.number_input("Stock", min_value=0, value=p["stock"])
                with col2:
                    precio_compra = st.number_input("Precio compra ($)", min_value=0.0,
                                                    value=float(p["precio_compra"]), step=0.10)
                    precio_venta = st.number_input("Precio venta ($)", min_value=0.0,
                                                   value=float(p["precio_venta"]), step=0.10)
                    stock_minimo = st.number_input("Stock mínimo", min_value=0, value=p["stock_minimo"])
                submitted = st.form_submit_button("💾 Guardar Cambios")
                if submitted:
                    ok, msg = modificar_producto(p["id"], codigo, nombre, stock, precio_compra, precio_venta, stock_minimo)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    
    with tab_baja:
        st.subheader("🗑️ Dar de Baja un Producto")
        prods = obtener_productos()
        if not prods:
            st.info("ℹ️ No hay productos para eliminar.")
        else:
            opciones = {f"{p['codigo']} - {p['nombre']}": p for p in prods}
            seleccionado = st.selectbox("Selecciona un producto a eliminar:", list(opciones.keys()), key="baja")
            p = opciones[seleccionado]
            st.warning(f"⚠️ ¿Estás seguro de eliminar **{p['nombre']}**?")
            if st.button("🗑️ Confirmar Eliminación", type="primary"):
                ok, msg = eliminar_producto(p["id"])
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


# ============================================================
# SECCIÓN: PUNTO DE VENTA
# ============================================================
elif seccion == "💰 Punto de Venta":
    st.header("💰 Punto de Venta - Mini Market Express")
    st.info("""
    ℹ️ **¿Cómo funciona?**  
    1. Selecciona el producto y la cantidad  
    2. Agrégalo al carrito  
    3. Presiona **Generar Ticket**  
    4. El stock se actualizará automáticamente
    """)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    prods = obtener_productos()
    opciones = {f"{p['codigo']} - {p['nombre']} (stock: {p['stock']}) - ${p['precio_venta']:.2f}": p for p in prods}
    
    with col1:
        seleccionado = st.selectbox("Producto:", list(opciones.keys()))
    with col2:
        cantidad = st.number_input("Cantidad:", min_value=1, value=1)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Agregar"):
            p = opciones[seleccionado]
            if p["stock"] < cantidad:
                st.error(f"❌ Stock insuficiente (disponible: {p['stock']})")
            else:
                st.session_state.carrito.append({
                    "producto_id": p["id"], "codigo": p["codigo"], "nombre": p["nombre"],
                    "cantidad": cantidad, "precio": p["precio_venta"],
                    "subtotal": p["precio_venta"] * cantidad
                })
                st.success(f"✅ {p['nombre']} x{cantidad} agregado")
                st.rerun()
    
    st.markdown("---")
    st.subheader("🛒 Carrito")
    if not st.session_state.carrito:
        st.info("ℹ️ El carrito está vacío.")
    else:
        tabla = "| Código | Producto | Cantidad | Precio | Subtotal |\n"
        tabla += "|--------|----------|----------|--------|----------|\n"
        total = 0
        for item in st.session_state.carrito:
            tabla += f"| {item['codigo']} | {item['nombre']} | {item['cantidad']} | ${item['precio']:.2f} | ${item['subtotal']:.2f} |\n"
            total += item["subtotal"]
        st.markdown(tabla)
        st.markdown(f"### 💵 **TOTAL: ${total:,.2f}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Vaciar Carrito"):
                st.session_state.carrito = []
                st.rerun()
        with col2:
            if st.button("✅ Generar Ticket", type="primary"):
                ok, msg, venta = registrar_venta(st.session_state.carrito)
                if ok:
                    st.session_state.carrito = []
                    st.session_state.ultima_venta = venta
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    if st.session_state.ultima_venta:
        venta = st.session_state.ultima_venta
        st.markdown("---")
        st.subheader("🧾 Ticket de Venta")
        st.code(f"""
============================================
          MINI MARKET EXPRESS
      Sistema de Gestión de Stock
============================================
Ticket N°: {venta['id']:05d}
Fecha: {venta['fecha']}
============================================
""")
        tabla_ticket = "| Producto | Cant. | Precio | Subtotal |\n"
        tabla_ticket += "|----------|-------|--------|----------|\n"
        for d in venta["items"]:
            tabla_ticket += f"| {d['nombre']} | {d['cantidad']} | ${d['precio_unitario']:.2f} | ${d['subtotal']:.2f} |\n"
        st.markdown(tabla_ticket)
        st.code(f"""
--------------------------------------------
TOTAL: ${venta['total']:,.2f}
============================================
     ¡Gracias por su compra!
============================================
""")
        if st.button("✔️ Cerrar Ticket"):
            st.session_state.ultima_venta = None
            st.rerun()


# ============================================================
# SECCIÓN: REPORTES
# ============================================================
elif seccion == "📊 Reportes":
    st.header("📊 Reportes y Análisis - Mini Market Express")
    tab1, tab2, tab3 = st.tabs(["📈 Ventas", "📦 Inventario", "⚠️ Stock Bajo"])
    
    with tab1:
        st.subheader("📈 Reporte de Ventas")
        ventas = st.session_state.ventas
        if not ventas:
            st.info("ℹ️ No hay ventas registradas todavía.")
        else:
            total_v = total_ventas()
            gan = ganancia_total()
            num_ventas = len(ventas)
            ticket_promedio = total_v / num_ventas if num_ventas else 0
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💰 Total Vendido", f"${total_v:,.2f}")
            col2.metric("📈 Ganancia", f"${gan:,.2f}")
            col3.metric("🧾 N° Ventas", num_ventas)
            col4.metric("📊 Ticket Promedio", f"${ticket_promedio:,.2f}")
            
            st.markdown("---")
            st.subheader("📋 Historial de Ventas")
            for v in reversed(ventas):
                with st.expander(f"🧾 Venta #{v['id']} — {v['fecha']} — ${v['total']:,.2f}"):
                    t = "| Producto | Cant. | Precio | Subtotal |\n"
                    t += "|----------|-------|--------|----------|\n"
                    for d in v["items"]:
                        t += f"| {d['nombre']} | {d['cantidad']} | ${d['precio_unitario']:.2f} | ${d['subtotal']:.2f} |\n"
                    st.markdown(t)
    
    with tab2:
        st.subheader("📦 Reporte de Inventario")
        prods = obtener_productos()
        vc, vv = valor_inventario()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📦 Total Productos", len(prods))
        col2.metric("💼 Valor Compra", f"${vc:,.2f}")
        col3.metric("💵 Valor Venta", f"${vv:,.2f}")
        
        st.markdown("---")
        tabla = "| Código | Producto | Stock | P.Compra | P.Venta | Valor |\n"
        tabla += "|--------|----------|-------|----------|---------|-------|\n"
        for p in prods:
            valor = p["stock"] * p["precio_compra"]
            tabla += f"| {p['codigo']} | {p['nombre']} | {p['stock']} | ${p['precio_compra']:.2f} | ${p['precio_venta']:.2f} | ${valor:.2f} |\n"
        st.markdown(tabla)
    
    with tab3:
        st.subheader("⚠️ Productos con Stock Bajo")
        bajos = productos_con_stock_bajo()
        if not bajos:
            st.success("✅ No hay productos con stock bajo.")
        else:
            for p in bajos:
                st.error(f"🔔 **{p['nombre']}** ({p['codigo']}) — Stock: **{p['stock']}** | Mínimo: **{p['stock_minimo']}**")
            
            st.markdown("---")
            st.subheader("💡 Sugerencia de Reposición")
            tabla = "| Producto | Stock Actual | Mínimo | Reponer |\n"
            tabla += "|----------|--------------|--------|---------|\n"
            for p in bajos:
                reponer = p["stock_minimo"] * 2 - p["stock"]
                tabla += f"| {p['nombre']} | {p['stock']} | {p['stock_minimo']} | {reponer} uds |\n"
            st.markdown(tabla)


# ============================================================
# SECCIÓN: ASISTENTE IA
# ============================================================
elif seccion == "🤖 Asistente IA":
    st.header("🤖 Asistente IA - Mini Market Express")
    st.info("""
    ℹ️ **¿Qué hace?**  
    Es un asistente que responde preguntas sobre tu inventario y ventas 
    usando lenguaje natural. Basado en reglas (sin ML).
    """)
    
    # Sugerencias rápidas
    st.subheader("💡 Consultas Rápidas")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚠️ Stock bajo"):
            st.session_state.consulta_ia = "¿Qué productos tienen stock bajo?"
        if st.button("💰 Total ventas"):
            st.session_state.consulta_ia = "¿Cuál es el total de ventas?"
    with col2:
        if st.button("📈 Ganancia"):
            st.session_state.consulta_ia = "¿Cuál es la ganancia?"
        if st.button("🏆 Más vendido"):
            st.session_state.consulta_ia = "¿Cuál es el producto más vendido?"
    with col3:
        if st.button("💼 Valor inventario"):
            st.session_state.consulta_ia = "¿Cuánto vale el inventario?"
        if st.button("🧠 Sugerencias"):
            st.session_state.consulta_ia = "Dame sugerencias"
    
    st.markdown("---")
    
    # Entrada de texto
    pregunta = st.text_input("Escribe tu consulta:", 
                             value=st.session_state.get("consulta_ia", ""),
                             placeholder="Ej: ¿Qué productos tienen stock bajo?")
    
    if st.button("🚀 Consultar", type="primary"):
        if pregunta:
            respuesta = responder_consulta(pregunta)
            st.markdown("---")
            st.subheader("🤖 Respuesta del Asistente")
            st.markdown(respuesta)
        else:
            st.warning("⚠️ Escribe una consulta primero")
    
    st.markdown("---")
    with st.expander("📖 Ver todas las consultas disponibles"):
        st.markdown("""
        | Consulta | Descripción |
        |----------|-------------|
        | ¿Qué productos tienen stock bajo? | Alertas de reposición |
        | ¿Cuál es el total de ventas? | Total vendido |
        | ¿Cuál es la ganancia? | Utilidad acumulada |
        | ¿Cuál es el producto más vendido? | Top ventas |
        | ¿Cuánto vale el inventario? | Valor del stock |
        | ¿Cuántos productos hay? | Total de productos |
        | Dame sugerencias | Recomendaciones inteligentes |
        """)


# ============================================================
# PIE DE PÁGINA
# ============================================================
st.markdown("---")
st.caption("🛒 Mini Market Express | Contáctenos por 0285-6312346 -- 0414-5432109 |Ciudad Bolivar - Venezuela")