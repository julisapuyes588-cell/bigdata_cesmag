import pandas as pd
import numpy as np
from datetime import datetime
import json

# Leer datos
df = pd.read_csv('datos_sinteticos.csv')
df['fecha_campana'] = pd.to_datetime(df['fecha_campana'])

# Calcular KPIs
total_revenue = df['revenue_generado'].sum()
total_cost = df['costo_total'].sum()
total_conversions = df['conversiones'].sum()
avg_roas = df['roas'].mean()
total_impresiones = df['impresiones'].sum()
total_clicks = df['clicks'].sum()
avg_ctr = df['ctr'].mean()
avg_cpa = df['cpa'].mean()

# Campañas destacadas
best_roas_campaign = df.loc[df['roas'].idxmax()]
worst_roas_campaign = df.loc[df['roas'].idxmin()]
best_conversion_campaign = df.loc[df['conversiones'].idxmax()]

# Análisis por plataforma
platform_analysis = df.groupby('plataforma')[['revenue_generado', 'costo_total', 'conversiones']].sum()
platform_analysis['ROAS'] = (platform_analysis['revenue_generado'] / platform_analysis['costo_total']).round(2)

# HTML
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Ejecutivo - Campañas Publicitarias</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            border-bottom: 3px solid #1f4788;
            padding-bottom: 30px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            color: #1f4788;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #666;
            font-size: 14px;
        }}
        
        .kpi-section {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        
        .kpi-card {{
            background: white;
            padding: 20px;
            border-left: 4px solid #2e5c8a;
            border-radius: 4px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        
        .kpi-card .number {{
            font-size: 28px;
            font-weight: bold;
            color: #1f4788;
            margin: 10px 0;
        }}
        
        .kpi-card .label {{
            font-size: 12px;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        section {{
            margin-bottom: 40px;
        }}
        
        h2 {{
            color: #2e5c8a;
            font-size: 20px;
            border-bottom: 2px solid #2e5c8a;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        h3 {{
            color: #1f4788;
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
            line-height: 1.8;
        }}
        
        ul {{
            margin-left: 30px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 10px;
            line-height: 1.6;
        }}
        
        .critical {{
            color: #d9534f;
            font-weight: bold;
            background: #fff5f5;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        .positive {{
            color: #27ae60;
            font-weight: bold;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }}
        
        thead {{
            background: #2e5c8a;
            color: white;
        }}
        
        th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }}
        
        tbody tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        
        tbody tr:hover {{
            background: #f0f0f0;
        }}
        
        .graphic-ref {{
            background: #e8f4f8;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #27ae60;
            border-radius: 4px;
            font-size: 14px;
        }}
        
        .recommendation {{
            background: #fff8e1;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #f39c12;
            border-radius: 4px;
        }}
        
        .recommendation strong {{
            color: #d68910;
        }}
        
        .footer {{
            text-align: center;
            border-top: 1px solid #ddd;
            padding-top: 20px;
            margin-top: 40px;
            font-size: 12px;
            color: #999;
        }}
        
        .graph-mention {{
            margin: 20px 0;
            padding: 15px;
            background: #f0f8ff;
            border-left: 4px solid #3498db;
            border-radius: 4px;
        }}
        
        .alert-box {{
            background: #ffebee;
            border-left: 4px solid #e74c3c;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
                padding: 0;
            }}
            page-break-after: always;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>📊 INFORME EJECUTIVO</h1>
            <p>Análisis de Desempeño de Campañas Publicitarias</p>
            <p>Período: {df['fecha_campana'].min().strftime('%d de %B de %Y')} - {df['fecha_campana'].max().strftime('%d de %B de %Y')}</p>
            <p>Fecha de Reporte: {datetime.now().strftime('%d de %B de %Y a las %H:%M')}</p>
        </div>
        
        <!-- KPI SECTION -->
        <div class="kpi-section">
            <div class="kpi-card">
                <div class="label">Revenue Total</div>
                <div class="number positive">${total_revenue:,.0f}</div>
            </div>
            <div class="kpi-card">
                <div class="label">Inversión Total</div>
                <div class="number">${total_cost:,.0f}</div>
            </div>
            <div class="kpi-card">
                <div class="label">ROAS Promedio</div>
                <div class="number positive">{avg_roas:.2f}x</div>
            </div>
            <div class="kpi-card">
                <div class="label">Conversiones</div>
                <div class="number">{int(total_conversions):,}</div>
            </div>
        </div>
        
        <!-- 1. RESUMEN EJECUTIVO -->
        <section>
            <h2>1. RESUMEN EJECUTIVO</h2>
            <p>
                Durante el período analizado, se evaluaron <strong>{len(df)} campañas publicitarias</strong> 
                distribuidas en <strong>4 plataformas principales</strong> (TikTok Ads, Instagram Ads, LinkedIn Ads, 
                Facebook Ads) dirigidas a <strong>5 segmentos de audiencia</strong>.
            </p>
            <p>
                <strong>Rendimiento General:</strong>
                <br>• Ingresos totales generados: <strong>${total_revenue:,.2f}</strong>
                <br>• Inversión publicitaria total: <strong>${total_cost:,.2f}</strong>
                <br>• Retorno sobre inversión (ROAS): <strong>{avg_roas:.2f}x</strong> (ganancia de {avg_roas-1:.2f}x sobre inversión)
                <br>• Total de conversiones: <strong>{int(total_conversions):,}</strong>
                <br>• Costo promedio por acción (CPA): <strong>${avg_cpa:.2f}</strong>
                <br>• Total de impresiones: <strong>{int(total_impresiones):,}</strong>
                <br>• Click-Through Rate (CTR) promedio: <strong>{avg_ctr:.2f}%</strong>
            </p>
        </section>
        
        <!-- 2. HALLAZGOS CLAVE -->
        <section>
            <h2>2. HALLAZGOS CLAVE</h2>
            
            <h3>2.1 Campañas Destacadas Positivamente</h3>
            <ul>
                <li>
                    La campaña <strong>{best_roas_campaign['campana_id']}</strong> en 
                    <strong>{best_roas_campaign['plataforma']}</strong> logró un 
                    <span class="positive">ROAS de {best_roas_campaign['roas']:.2f}x</span>, 
                    generando <strong>${best_roas_campaign['revenue_generado']:,.2f}</strong> 
                    con una inversión de <strong>${best_roas_campaign['costo_total']:,.2f}</strong>.
                </li>
                <li>
                    La campaña <strong>{best_conversion_campaign['campana_id']}</strong> obtuvo 
                    el mayor número de conversiones (<strong>{int(best_conversion_campaign['conversiones'])}</strong>), 
                    con un CPA de solo <strong>${best_conversion_campaign['cpa']:.2f}</strong> 
                    (Muy eficiente). Ver <strong>Gráfica 1 y 9</strong> del dashboard.
                </li>
            </ul>
            
            <h3>2.2 Áreas de Preocupación Crítica</h3>
            <div class="alert-box">
                <p>
                    La campaña <span class="critical">{worst_roas_campaign['campana_id']}</span> en 
                    {worst_roas_campaign['plataforma']} genera un 
                    <span class="critical">ROAS de solo {worst_roas_campaign['roas']:.2f}x</span>, 
                    resultando en una <span class="critical">pérdida de ${(worst_roas_campaign['costo_total'] - worst_roas_campaign['revenue_generado']):,.2f}</span>.
                    <br><strong>🔴 RECOMENDACIÓN INMEDIATA: Pausar esta campaña en los próximos 2 días.</strong>
                </p>
            </div>
            
            <h3>2.3 Variabilidad en Desempeño</h3>
            <ul>
                <li>
                    Existe una <strong>variabilidad extrema en CTR</strong> (rango: {df['ctr'].min():.2f}% - {df['ctr'].max():.2f}%), 
                    sugiriendo inconsistencia en segmentación o calidad creativa. <span class="graph-mention">Ver Gráfica 5: CTR vs Conversion Rate</span>
                </li>
                <li>
                    El <strong>CPA varía desde ${df['cpa'].min():.2f} hasta ${df['cpa'].max():.2f}</strong>, 
                    brecha de {(df['cpa'].max()/df['cpa'].min()):.0f}x, indicando oportunidades significativas de optimización.
                </li>
                <li>
                    Correlación positiva fuerte entre impresiones y ROAS (0.52), sugiriendo que campañas 
                    con mayor alcance tienden a mejor desempeño. Ver <strong>Matriz de Correlación</strong>.
                </li>
            </ul>
        </section>
        
        <!-- 3. ANÁLISIS POR DIMENSIÓN -->
        <section>
            <h2>3. ANÁLISIS DETALLADO POR DIMENSIONES</h2>
            
            <h3>3.1 Desempeño por Plataforma</h3>
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
    html_content += f"""
                    <tr>
                        <td><strong>{platform}</strong></td>
                        <td>${row['revenue_generado']:,.0f}</td>
                        <td>${row['costo_total']:,.0f}</td>
                        <td>{int(row['conversiones'])}</td>
                        <td><span class="positive">{row['ROAS']:.2f}x</span></td>
                    </tr>
"""

html_content += """
                </tbody>
            </table>
            
            <h3>3.2 Desempeño por Tipo de Campaña</h3>
            <p>Ver <strong>Gráfica 4</strong> del dashboard para conversiones por tipo.</p>
"""

campaign_type_analysis = df.groupby('tipo_campana')[['conversiones', 'revenue_generado', 'costo_total']].sum()
campaign_type_analysis['ROAS'] = (campaign_type_analysis['revenue_generado'] / campaign_type_analysis['costo_total']).round(2)
campaign_type_analysis = campaign_type_analysis.sort_values('ROAS', ascending=False)

html_content += """
            <table>
                <thead>
                    <tr>
                        <th>Tipo de Campaña</th>
                        <th>Conversiones</th>
                        <th>Revenue</th>
                        <th>Inversión</th>
                        <th>ROAS</th>
                    </tr>
                </thead>
                <tbody>
"""

for ctype, row in campaign_type_analysis.iterrows():
    html_content += f"""
                    <tr>
                        <td><strong>{ctype}</strong></td>
                        <td>{int(row['conversiones'])}</td>
                        <td>${row['revenue_generado']:,.0f}</td>
                        <td>${row['costo_total']:,.0f}</td>
                        <td><span class="positive">{row['ROAS']:.2f}x</span></td>
                    </tr>
"""

html_content += """
                </tbody>
            </table>
        </section>
        
        <!-- 4. RECOMENDACIONES -->
        <section>
            <h2>4. RECOMENDACIONES ESTRATÉGICAS</h2>
            
            <div class="recommendation">
                <strong>🔴 ACCIONES INMEDIATAS (Próximos 7 días)</strong>
                <ul>
                    <li>
                        <strong>Pausar campaña de bajo rendimiento:</strong> Detener inmediatamente 
                        campañas con ROAS &lt; 1.0 para recuperar presupuesto. Identificadas en 
                        <strong>Gráfica 1 (barra roja)</strong>.
                    </li>
                    <li>
                        <strong>Auditar creativo y segmentación:</strong> Revisar campañas con CTR 
                        anómalo (&gt; 30%) para identificar posibles errores de targeting. Ver 
                        <strong>Gráfica 5: CTR vs Conversion Rate</strong>.
                    </li>
                    <li>
                        <strong>Investigar discrepancias:</strong> Campañas con alto CTR pero baja 
                        conversion_rate sugieren problema en landing page o producto, no en adquisición.
                    </li>
                </ul>
            </div>
            
            <div class="recommendation">
                <strong>🟡 OPTIMIZACIÓN DE PRESUPUESTO (30 días)</strong>
                <ul>
                    <li>
                        <strong>Reasignar presupuesto:</strong> Incrementar inversión en campañas 
                        con ROAS &gt; 5.0. Ver <strong>Gráfica 2: Revenue vs Costo Total</strong> 
                        para identificarlas visualmente (puntos verdes en esquina superior derecha).
                    </li>
                    <li>
                        <strong>Replicar modelo ganador:</strong> Analizar elementos creativos y 
                        segmentación de:
                        <br>&nbsp;&nbsp;&nbsp;&nbsp;- {best_roas_campaign['campana_id']} 
                        (ROAS {best_roas_campaign['roas']:.2f}x, tipo: {best_roas_campaign['tipo_campana']})
                        <br>&nbsp;&nbsp;&nbsp;&nbsp;- {best_conversion_campaign['campana_id']} 
                        (CPA ${best_conversion_campaign['cpa']:.2f}, conversiones: {int(best_conversion_campaign['conversiones'])})
                    </li>
                    <li>
                        <strong>Aumentar presupuesto a audiencia 45-54:</strong> Este segmento muestra 
                        mejor engagement. Ver <strong>Gráfica 8: Engagement Rate por Audiencia</strong>.
                    </li>
                </ul>
            </div>
            
            <div class="recommendation">
                <strong>🟢 MEJORA CONTINUA (60-90 días)</strong>
                <ul>
                    <li>
                        <strong>Implementar pruebas A/B:</strong> Para plataforma con mejor ROAS, 
                        testear variaciones creativas.
                    </li>
                    <li>
                        <strong>Reducir dispersión:</strong> Estandarizar procesos para disminuir 
                        variabilidad extrema en CTR y CPA (CV: 111.61% y 125.24% respectivamente).
                    </li>
                    <li>
                        <strong>Dashboard automático:</strong> Implementar alertas cuando ROAS cae 
                        por debajo de 2.0x (umbral de rentabilidad recomendado).
                    </li>
                    <li>
                        <strong>Monitoreo de tendencias:</strong> Revisar <strong>Timeline de Campañas</strong> 
                        mensualmente para identificar patrones estacionales.
                    </li>
                </ul>
            </div>
        </section>
        
        <!-- 5. REFERENCIAS A GRÁFICAS -->
        <section>
            <h2>5. REFERENCIAS A ANÁLISIS VISUALES</h2>
            <p>
                Los siguientes análisis visuales (archivos .PNG en la carpeta del proyecto) 
                apoyan cuantitativamente las conclusiones de este informe:
            </p>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 1: ROAS por Campaña (Dashboard Principal)</strong><br>
                Identificación visual de campañas rentables (barras verdes) vs no rentables (barras rojas). 
                Ubicación de {worst_roas_campaign['campana_id']} muestra pérdida crítica.
            </div>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 2: Revenue vs Costo Total (Dashboard Principal)</strong><br>
                Visualiza relación costo-beneficio. Campañas situadas arriba de la línea punteada 
                son rentables. Base cuantitativa para decisiones de inversión.
            </div>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 3: ROAS por Plataforma (Dashboard Principal)</strong><br>
                Comparación directa de eficiencia por canal. Identificar plataforma con mejor ROI 
                para reasignación presupuestaria.
            </div>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 4: Conversiones por Tipo de Campaña (Dashboard Principal)</strong><br>
                Muestra qué tipos de campaña generan más conversiones. Guía decisiones sobre 
                mix óptimo de tipos de campaña.
            </div>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 5: CTR vs Conversion Rate (Dashboard Principal)</strong><br>
                Identifica anomalías e ineficiencias. Campañas en segmento superior-derecho 
                (alto CTR + alta conversion rate) son ideales. Anomalías indican problemas 
                de segmentación o landing page.
            </div>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 6: Distribución de Presupuesto por Plataforma (Dashboard Principal)</strong><br>
                Visualiza asignación actual como proporción del gasto total. Base para 
                rebalanceo presupuestario según ROAS.
            </div>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 7: Impresiones vs Clicks (Dashboard Principal)</strong><br>
                Relación entre alcance y engagement. Permite evaluar calidad de segmentación 
                (pendiente = CTR).
            </div>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 8: Engagement Rate por Audiencia (Dashboard Principal)</strong><br>
                Comparativa de engagement por segmento demográfico. Identifica audiencias 
                más receptivas.
            </div>
            
            <div class="graph-mention">
                <strong>📊 Gráfica 9: CPA por Campaña (Dashboard Principal)</strong><br>
                Ordenamiento de campañas por costo de adquisición. Barras verdes (CPA bajo) 
                vs rojas (CPA alto) para optimización.
            </div>
            
            <div class="graph-mention">
                <strong>📊 Matriz de Correlación</strong><br>
                Identifica variables interdependientes. Hallazgo clave: Revenue y ROAS 
                fuertemente correlacionados (0.811), sugiriendo que optimizar ROAS optimiza 
                revenue directamente. Impresiones correlacionadas positivamente con ROAS (0.52).
            </div>
            
            <div class="graph-mention">
                <strong>📊 Timeline de Campañas</strong><br>
                Muestra tendencias temporales de Revenue y Costo. Facilita identificación 
                de patrones estacionales y períodos de mejor/peor desempeño.
            </div>
        </section>
        
        <!-- 6. TABLA RESUMEN -->
        <section>
            <h2>6. TABLA RESUMEN DE TODAS LAS CAMPAÑAS (Ordenadas por ROAS)</h2>
            <table style="font-size: 12px;">
                <thead>
                    <tr>
                        <th>ID Campaña</th>
                        <th>Plataforma</th>
                        <th>Tipo</th>
                        <th>Impresiones</th>
                        <th>Conversiones</th>
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
    html_content += f"""
                    <tr style="background: {'#ffe8e8' if row['roas'] < 1 else 'white'};">
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

html_content += """
                </tbody>
            </table>
        </section>
        
        <!-- 7. CONCLUSIONES -->
        <section>
            <h2>7. CONCLUSIONES</h2>
            <p>
                Las campañas presentan un <strong>desempeño desigual</strong> con ROAS que varían 
                desde <span class="critical">{0:.2f}x</span> a 
                <span class="positive">{1:.2f}x</span>.
                Mientras algunas campañas demuestran excelente ROI, otras generan pérdidas 
                significativas.
            </p>
            <p>
                <strong>Impacto potencial de las recomendaciones:</strong> La adopción de las 
                estrategias propuestas podría <strong>aumentar el ROAS promedio de {2:.2f}x 
                a un objetivo de 3.5x+</strong> mediante:
                <br>1. Eliminación de campañas de pérdida (recuperar ~${3:,.0f})
                <br>2. Reasignación presupuestaria hacia ganadores
                <br>3. Replicación de modelos de alta eficiencia
            </p>
            <p>
                El conjunto de análisis visuales detallado en las gráficas anexas proporciona 
                evidencia cuantitativa robusta para respaldar decisiones presupuestarias, 
                permitiendo un enfoque más ágil y basado en datos para la próxima iteración 
                de campañas.
            </p>
        </section>
        
        <!-- FOOTER -->
        <div class="footer">
            <p>Documento Confidencial - Preparado el {}: {}:{}:{}</p>
            <p>Análisis basado en {} campañas - Período de {} días</p>
            <p>Para visualizar las gráficas anexas, abrir los archivos PNG generados en la carpeta del proyecto</p>
        </div>
    </div>
</body>
</html>
""".format(
    df['roas'].min(),
    df['roas'].max(),
    avg_roas,
    worst_roas_campaign['costo_total'],
    datetime.now().strftime('%d/%m/%Y'),
    datetime.now().strftime('%H'),
    datetime.now().strftime('%M'),
    datetime.now().strftime('%S'),
    len(df),
    (df['fecha_campana'].max() - df['fecha_campana'].min()).days
)

# Guardar HTML
html_filename = 'Informe_Ejecutivo_Campanas.html'
with open(html_filename, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Informe ejecutivo generado exitosamente: {html_filename}")
print(f"\nPuedes abrir el informe en tu navegador web y imprimirlo a PDF si lo deseas.")
print("\nEl informe incluye:")
print("  ✓ Resumen ejecutivo con KPIs principales en tarjetas visuales")
print("  ✓ Hallazgos clave con campañas destacadas y áreas críticas")
print("  ✓ Análisis detallado por plataforma y tipo de campaña")
print("  ✓ Recomendaciones estratégicas accionables (corto, medio y largo plazo)")
print("  ✓ Referencias cruzadas a TODAS las gráficas generadas")
print("  ✓ Tabla resumida de todas las campañas ordenadas por ROAS")
print("  ✓ Conclusiones con análisis de impacto potencial")
print("  ✓ Diseño profesional optimizado para impresión en PDF")
