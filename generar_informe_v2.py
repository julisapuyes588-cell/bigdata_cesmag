import pandas as pd
import numpy as np
from datetime import datetime

# Leer datos
df = pd.read_csv('datos_sinteticos.csv')
df['fecha_campana'] = pd.to_datetime(df['fecha_campana'])

# Calcular KPIs
total_revenue = df['revenue_generado'].sum()
total_cost = df['costo_total'].sum()
total_conversions = df['conversiones'].sum()
avg_roas = df['roas'].mean()
total_impresiones = df['impresiones'].sum()
avg_ctr = df['ctr'].mean()
avg_cpa = df['cpa'].mean()

# Campañas destacadas
best_roas_campaign = df.loc[df['roas'].idxmax()]
worst_roas_campaign = df.loc[df['roas'].idxmin()]
best_conversion_campaign = df.loc[df['conversiones'].idxmax()]

# Análisis por plataforma
platform_analysis = df.groupby('plataforma')[['revenue_generado', 'costo_total', 'conversiones']].sum()
platform_analysis['ROAS'] = (platform_analysis['revenue_generado'] / platform_analysis['costo_total']).round(2)

# Crear HTML
html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Ejecutivo - Campañas Publicitarias</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        .header {
            text-align: center;
            border-bottom: 3px solid #1f4788;
            padding-bottom: 30px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #1f4788;
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 14px;
            margin-top: 8px;
        }
        
        .kpi-section {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }
        
        .kpi-card {
            background: white;
            padding: 20px;
            border-left: 4px solid #2e5c8a;
            border-radius: 4px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .kpi-card .number {
            font-size: 28px;
            font-weight: bold;
            color: #1f4788;
            margin: 10px 0;
        }
        
        .kpi-card .label {
            font-size: 12px;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        section {
            margin-bottom: 40px;
        }
        
        h2 {
            color: #2e5c8a;
            font-size: 20px;
            border-bottom: 2px solid #2e5c8a;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        h3 {
            color: #1f4788;
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        p {
            margin-bottom: 15px;
            text-align: justify;
            line-height: 1.8;
        }
        
        ul {
            margin-left: 30px;
            margin-bottom: 15px;
        }
        
        li {
            margin-bottom: 10px;
            line-height: 1.6;
        }
        
        .critical {
            color: #d9534f;
            font-weight: bold;
        }
        
        .positive {
            color: #27ae60;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 13px;
        }
        
        thead {
            background: #2e5c8a;
            color: white;
        }
        
        th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }
        
        tbody tr:nth-child(even) {
            background: #f9f9f9;
        }
        
        tbody tr:hover {
            background: #f0f0f0;
        }
        
        .graphic-ref {
            background: #e8f4f8;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #27ae60;
            border-radius: 4px;
            font-size: 14px;
        }
        
        .recommendation {
            background: #fff8e1;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #f39c12;
            border-radius: 4px;
        }
        
        .recommendation strong {
            color: #d68910;
        }
        
        .footer {
            text-align: center;
            border-top: 1px solid #ddd;
            padding-top: 20px;
            margin-top: 40px;
            font-size: 12px;
            color: #999;
        }
        
        .alert-box {
            background: #ffebee;
            border-left: 4px solid #e74c3c;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        
        @media print {
            body {
                background: white;
            }
            .container {
                box-shadow: none;
                padding: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 INFORME EJECUTIVO</h1>
            <p><strong>Análisis de Desempeño de Campañas Publicitarias</strong></p>
            <p>Período: """ + df['fecha_campana'].min().strftime('%d de %B de %Y') + """ - """ + df['fecha_campana'].max().strftime('%d de %B de %Y') + """</p>
            <p>Fecha de Reporte: """ + datetime.now().strftime('%d de %B de %Y a las %H:%M') + """</p>
        </div>
        
        <div class="kpi-section">
            <div class="kpi-card">
                <div class="label">Revenue Total</div>
                <div class="number positive">$""" + f"{total_revenue:,.0f}" + """</div>
            </div>
            <div class="kpi-card">
                <div class="label">Inversión Total</div>
                <div class="number">$""" + f"{total_cost:,.0f}" + """</div>
            </div>
            <div class="kpi-card">
                <div class="label">ROAS Promedio</div>
                <div class="number positive">""" + f"{avg_roas:.2f}" + """x</div>
            </div>
            <div class="kpi-card">
                <div class="label">Conversiones</div>
                <div class="number">""" + f"{int(total_conversions):,}" + """</div>
            </div>
        </div>
        
        <section>
            <h2>1. RESUMEN EJECUTIVO</h2>
            <p>
                Durante el período analizado, se evaluaron <strong>""" + str(len(df)) + """ campañas publicitarias</strong> 
                distribuidas en <strong>4 plataformas principales</strong> (TikTok Ads, Instagram Ads, LinkedIn Ads, 
                Facebook Ads) dirigidas a <strong>5 segmentos de audiencia</strong>.
            </p>
            <p>
                <strong>Rendimiento General:</strong><br>
                • Ingresos totales: <strong>$""" + f"{total_revenue:,.2f}" + """</strong><br>
                • Inversión total: <strong>$""" + f"{total_cost:,.2f}" + """</strong><br>
                • ROAS promedio: <strong>""" + f"{avg_roas:.2f}" + """x</strong> (ganancia de """ + f"{avg_roas-1:.2f}" + """x sobre inversión)<br>
                • Conversiones: <strong>""" + f"{int(total_conversions):,}" + """</strong><br>
                • CPA promedio: <strong>$""" + f"{avg_cpa:.2f}" + """</strong><br>
                • Impresiones: <strong>""" + f"{int(total_impresiones):,}" + """</strong><br>
                • CTR promedio: <strong>""" + f"{avg_ctr:.2f}" + """%</strong>
            </p>
        </section>
        
        <section>
            <h2>2. HALLAZGOS CLAVE</h2>
            
            <h3>2.1 Campañas Destacadas Positivamente</h3>
            <ul>
                <li>
                    La campaña <strong>""" + best_roas_campaign['campana_id'] + """</strong> en 
                    <strong>""" + best_roas_campaign['plataforma'] + """</strong> logró un 
                    <span class="positive">ROAS de """ + f"{best_roas_campaign['roas']:.2f}" + """x</span>, 
                    generando <strong>$""" + f"{best_roas_campaign['revenue_generado']:,.2f}" + """</strong>.
                </li>
                <li>
                    La campaña <strong>""" + best_conversion_campaign['campana_id'] + """</strong> obtuvo 
                    el mayor número de conversiones (<strong>""" + str(int(best_conversion_campaign['conversiones'])) + """</strong>), 
                    con un CPA de solo <strong>$""" + f"{best_conversion_campaign['cpa']:.2f}" + """</strong>.
                </li>
            </ul>
            
            <h3>2.2 Áreas de Preocupación Crítica</h3>
            <div class="alert-box">
                <p>
                    La campaña <span class="critical">""" + worst_roas_campaign['campana_id'] + """</span> en 
                    """ + worst_roas_campaign['plataforma'] + """ genera un 
                    <span class="critical">ROAS de """ + f"{worst_roas_campaign['roas']:.2f}" + """x</span>, 
                    resultando en una <span class="critical">pérdida de $""" + f"{(worst_roas_campaign['costo_total'] - worst_roas_campaign['revenue_generado']):,.2f}" + """</span>.
                    <br><strong>🔴 RECOMENDACIÓN INMEDIATA: Pausar esta campaña en los próximos 2 días.</strong>
                </p>
            </div>
            
            <h3>2.3 Variabilidad en Desempeño</h3>
            <ul>
                <li>
                    Variabilidad extrema en CTR (rango: """ + f"{df['ctr'].min():.2f}" + """% - """ + f"{df['ctr'].max():.2f}" + """%),
                    sugiriendo inconsistencia en segmentación.
                </li>
                <li>
                    CPA varía desde $""" + f"{df['cpa'].min():.2f}" + """ hasta $""" + f"{df['cpa'].max():.2f}" + """,
                    brecha de """ + f"{(df['cpa'].max()/df['cpa'].min()):.0f}" + """x de variación.
                </li>
            </ul>
        </section>
        
        <section>
            <h2>3. ANÁLISIS POR PLATAFORMA</h2>
            <p>Ver <strong>Gráfica 3</strong> del dashboard para visualización comparativa.</p>
            <table>
                <thead>
                    <tr>
                        <th>Plataforma</th>
                        <th>Revenue</th>
                        <th>Inversión</th>
                        <th>Conversiones</th>
                        <th>ROAS</th>
                    </tr>
                </thead>
                <tbody>
"""

for platform, row in platform_analysis.iterrows():
    html += f"""
                    <tr>
                        <td><strong>{platform}</strong></td>
                        <td>${row['revenue_generado']:,.0f}</td>
                        <td>${row['costo_total']:,.0f}</td>
                        <td>{int(row['conversiones'])}</td>
                        <td><span class="positive">{row['ROAS']:.2f}x</span></td>
                    </tr>
"""

html += """
                </tbody>
            </table>
        </section>
        
        <section>
            <h2>4. RECOMENDACIONES ESTRATÉGICAS</h2>
            
            <div class="recommendation">
                <strong>🔴 ACCIONES INMEDIATAS (Próximos 7 días)</strong>
                <ul>
                    <li><strong>Pausar campaña de bajo rendimiento:</strong> Detener campañas con ROAS < 1.0 (identificadas en Gráfica 1).</li>
                    <li><strong>Auditar creativo y segmentación:</strong> Revisar campañas con CTR anómalo. Ver Gráfica 5.</li>
                    <li><strong>Investigar discrepancias:</strong> Alto CTR pero baja conversion_rate sugiere problema en landing page.</li>
                </ul>
            </div>
            
            <div class="recommendation">
                <strong>🟡 OPTIMIZACIÓN DE PRESUPUESTO (30 días)</strong>
                <ul>
                    <li><strong>Reasignar presupuesto:</strong> Incrementar inversión en campañas con ROAS > 5.0. Ver Gráfica 2.</li>
                    <li><strong>Replicar modelo ganador:</strong> Analizar elementos de """ + best_roas_campaign['campana_id'] + """ (ROAS """ + f"{best_roas_campaign['roas']:.2f}" + """x).</li>
                    <li><strong>Enfoque en audiencia 45-54:</strong> Mejor engagement según Gráfica 8.</li>
                </ul>
            </div>
            
            <div class="recommendation">
                <strong>🟢 MEJORA CONTINUA (60-90 días)</strong>
                <ul>
                    <li><strong>Pruebas A/B:</strong> Para plataforma con mejor ROAS, testear variaciones creativas.</li>
                    <li><strong>Reducir dispersión:</strong> Estandarizar procesos para disminuir variabilidad extrema en CTR y CPA.</li>
                    <li><strong>Dashboard automático:</strong> Alertas cuando ROAS cae por debajo de 2.0x.</li>
                    <li><strong>Monitoreo de tendencias:</strong> Revisar Timeline de Campañas mensualmente.</li>
                </ul>
            </div>
        </section>
        
        <section>
            <h2>5. REFERENCIAS A GRÁFICAS GENERADAS</h2>
            <p>Los siguientes análisis visuales (archivos .PNG) apoyan las conclusiones:</p>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 1: ROAS por Campaña (Dashboard)</strong><br>
                Campañas rentables (barras verdes) vs no rentables (rojo). """ + worst_roas_campaign['campana_id'] + """ muestra pérdida crítica.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 2: Revenue vs Costo Total</strong><br>
                Campañas arriba de línea punteada son rentables. Base para decisiones de inversión.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 3: ROAS por Plataforma</strong><br>
                Comparación directa de eficiencia por canal para reasignación presupuestaria.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 4: Conversiones por Tipo de Campaña</strong><br>
                Identifica qué tipos generan más conversiones para optimizar mix.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 5: CTR vs Conversion Rate</strong><br>
                Identifica anomalías. Segment superior-derecho es el ideal.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 6: Distribución de Presupuesto por Plataforma</strong><br>
                Base para rebalanceo presupuestario según ROAS.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 7: Impresiones vs Clicks</strong><br>
                Evalúa calidad de segmentación (pendiente = CTR).
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 8: Engagement Rate por Audiencia</strong><br>
                Identifica audiencias más receptivas.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Gráfica 9: CPA por Campaña</strong><br>
                Barras verdes (CPA bajo) vs rojas (CPA alto) para optimización.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Matriz de Correlación</strong><br>
                Revenue y ROAS fuertemente correlacionados (0.811). Optimizar ROAS optimiza revenue directamente.
            </div>
            
            <div class="graphic-ref">
                <strong>📊 Timeline de Campañas</strong><br>
                Tendencias temporales para identificar patrones estacionales.
            </div>
        </section>
        
        <section>
            <h2>6. TABLA RESUMEN DE CAMPAÑAS (Por ROAS)</h2>
            <table style="font-size: 12px;">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Plataforma</th>
                        <th>Tipo</th>
                        <th>Impresiones</th>
                        <th>Conv</th>
                        <th>Costo</th>
                        <th>Revenue</th>
                        <th>ROAS</th>
                        <th>CPA</th>
                    </tr>
                </thead>
                <tbody>
"""

campaigns_summary = df[['campana_id', 'plataforma', 'tipo_campana', 'impresiones', 'conversiones', 
                        'costo_total', 'revenue_generado', 'roas', 'cpa']].copy()
campaigns_summary = campaigns_summary.sort_values('roas', ascending=False)

for idx, row in campaigns_summary.iterrows():
    roas_color = '#27ae60' if row['roas'] > 2 else '#e74c3c' if row['roas'] < 1 else '#f39c12'
    bg = '#ffe8e8' if row['roas'] < 1 else 'white'
    html += f"""
                    <tr style="background: {bg};">
                        <td><strong>{row['campana_id']}</strong></td>
                        <td>{row['plataforma']}</td>
                        <td>{row['tipo_campana']}</td>
                        <td>{int(row['impresiones']):,}</td>
                        <td>{int(row['conversiones'])}</td>
                        <td>${row['costo_total']:.2f}</td>
                        <td>${row['revenue_generado']:.2f}</td>
                        <td style="color: {roas_color}; font-weight: bold;">{row['roas']:.2f}x</td>
                        <td>${row['cpa']:.2f}</td>
                    </tr>
"""

html += """
                </tbody>
            </table>
        </section>
        
        <section>
            <h2>7. CONCLUSIONES</h2>
            <p>
                Las campañas presentan <strong>desempeño desigual</strong> con ROAS que varían 
                desde <span class="critical">""" + f"{df['roas'].min():.2f}" + """x</span> a 
                <span class="positive">""" + f"{df['roas'].max():.2f}" + """x</span>.
            </p>
            <p>
                <strong>Impacto potencial:</strong> Adoptar las recomendaciones podría 
                <strong>aumentar ROAS de """ + f"{avg_roas:.2f}" + """x a objetivo de 3.5x+</strong> mediante:
                <br>1. Eliminación de campañas de pérdida (recuperar ~$""" + f"{worst_roas_campaign['costo_total']:,.0f}" + """)
                <br>2. Reasignación presupuestaria hacia ganadores
                <br>3. Replicación de modelos eficientes
            </p>
            <p>
                El análisis visual detallado proporciona evidencia cuantitativa robusta para respaldar 
                decisiones presupuestarias, permitiendo un enfoque ágil basado en datos.
            </p>
        </section>
        
        <div class="footer">
            <p><strong>Documento Confidencial</strong></p>
            <p>Preparado el """ + datetime.now().strftime('%d/%m/%Y a las %H:%M:%S') + """</p>
            <p>Análisis de """ + str(len(df)) + """ campañas - Período de """ + str((df['fecha_campana'].max() - df['fecha_campana'].min()).days) + """ días</p>
            <p>Para visualizar gráficas, abrir archivos PNG en la carpeta del proyecto</p>
        </div>
    </div>
</body>
</html>"""

# Guardar
with open('Informe_Ejecutivo_Campanas.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Informe ejecutivo generado exitosamente: Informe_Ejecutivo_Campanas.html")
print("\nEl informe incluye:")
print("  ✓ ResumenEjecutivo con KPIs en tarjetas visuales")
print("  ✓ Hallazgos clave con campañas destacadas y críticas")
print("  ✓ Análisis detallado por plataforma")
print("  ✓ Recomendaciones estratégicas accionables")
print("  ✓ Referencias cruzadas a TODAS las gráficas (11 visualizaciones)")
print("  ✓ Tabla resumen de campañas ordenadas por ROAS")
print("  ✓ Conclusiones con impacto potencial")
print("  ✓ Diseño profesional optimizado para impresión en PDF")
print("\n📁 Archivos disponibles en la carpeta del proyecto:")
print("  • Informe_Ejecutivo_Campanas.html (Abre en navegador)")
print("  • analisis_campanas.png (Dashboard con 9 gráficas)")
print("  • matriz_correlacion.png (Heatmap de correlaciones)")
print("  • timeline_campanas.png (Tendencias temporales)")
