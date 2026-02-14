import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 12)
plt.rcParams['font.size'] = 10

# Leer el archivo CSV
df = pd.read_csv('datos_sinteticos.csv')
df['fecha_campana'] = pd.to_datetime(df['fecha_campana'])

# Crear figura con múltiples subplots
fig = plt.figure(figsize=(16, 14))

# 1. Distribución de ROAS por campaña
ax1 = plt.subplot(3, 3, 1)
roas_sorted = df.sort_values('roas')
colors = ['red' if x < 1 else 'green' for x in roas_sorted['roas']]
ax1.barh(roas_sorted['campana_id'], roas_sorted['roas'], color=colors, alpha=0.7)
ax1.axvline(x=1, color='black', linestyle='--', linewidth=2, label='ROAS = 1 (break-even)')
ax1.set_xlabel('ROAS')
ax1.set_title('ROAS por Campaña\n(Rojo: Pérdida, Verde: Ganancia)', fontweight='bold')
ax1.legend()

# 2. Revenue vs Costo Total
ax2 = plt.subplot(3, 3, 2)
ax2.scatter(df['costo_total'], df['revenue_generado'], s=200, alpha=0.6, c=df['roas'], cmap='RdYlGn')
ax2.plot([0, df['costo_total'].max()], [0, df['costo_total'].max()], 'k--', label='Break-even')
for idx, row in df.iterrows():
    ax2.annotate(row['campana_id'], (row['costo_total'], row['revenue_generado']), fontsize=7)
ax2.set_xlabel('Costo Total')
ax2.set_ylabel('Revenue Generado')
ax2.set_title('Revenue vs Costo Total\n(Color: ROAS)', fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Performance por Plataforma
ax3 = plt.subplot(3, 3, 3)
plataforma_kpis = df.groupby('plataforma')[['revenue_generado', 'costo_total']].sum()
plataforma_kpis['ROAS'] = plataforma_kpis['revenue_generado'] / plataforma_kpis['costo_total']
plataforma_kpis['ROAS'].sort_values().plot(kind='barh', ax=ax3, color='steelblue', alpha=0.7)
ax3.axvline(x=1, color='red', linestyle='--', linewidth=2)
ax3.set_xlabel('ROAS')
ax3.set_title('ROAS Promedio por Plataforma', fontweight='bold')

# 4. Conversiones por Tipo de Campaña
ax4 = plt.subplot(3, 3, 4)
conversiones_tipo = df.groupby('tipo_campana')['conversiones'].sum().sort_values()
conversiones_tipo.plot(kind='barh', ax=ax4, color='coral', alpha=0.7)
ax4.set_xlabel('Total de Conversiones')
ax4.set_title('Conversiones por Tipo de Campaña', fontweight='bold')

# 5. CTR vs Conversion Rate
ax5 = plt.subplot(3, 3, 5)
scatter = ax5.scatter(df['ctr'], df['conversion_rate'], s=200, c=df['roas'], cmap='RdYlGn', alpha=0.6, edgecolors='black')
for idx, row in df.iterrows():
    ax5.annotate(row['campana_id'], (row['ctr'], row['conversion_rate']), fontsize=7)
ax5.set_xlabel('CTR (%)')
ax5.set_ylabel('Conversion Rate (%)')
ax5.set_title('CTR vs Conversion Rate\n(Color: ROAS)', fontweight='bold')
plt.colorbar(scatter, ax=ax5, label='ROAS')

# 6. Distribución de Presupuesto por Plataforma
ax6 = plt.subplot(3, 3, 6)
presupuesto_plat = df.groupby('plataforma')['presupuesto_diario'].sum()
colors_pie = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
ax6.pie(presupuesto_plat, labels=presupuesto_plat.index, autopct='%1.1f%%', colors=colors_pie, startangle=90)
ax6.set_title('Distribución de Presupuesto\npor Plataforma', fontweight='bold')

# 7. Impresiones vs Clicks
ax7 = plt.subplot(3, 3, 7)
ax7.scatter(df['impresiones'], df['clicks'], s=200, alpha=0.6, c=df['ctr'], cmap='viridis')
ax7.set_xlabel('Impresiones')
ax7.set_ylabel('Clicks')
ax7.set_title('Impresiones vs Clicks\n(Color: CTR)', fontweight='bold')
for idx, row in df.iterrows():
    ax7.annotate(row['campana_id'], (row['impresiones'], row['clicks']), fontsize=7)

# 8. Engagement Rate por Audiencia
ax8 = plt.subplot(3, 3, 8)
engagement_aud = df.groupby('audiencia_objetivo')['engagement_rate'].mean().sort_values()
engagement_aud.plot(kind='barh', ax=ax8, color='mediumpurple', alpha=0.7)
ax8.set_xlabel('Engagement Rate Promedio (%)')
ax8.set_title('Engagement Rate por Audiencia', fontweight='bold')

# 9. CPA por Campaña (Top 10 mejor/peor)
ax9 = plt.subplot(3, 3, 9)
cpa_sorted = df.sort_values('cpa')[['campana_id', 'cpa']]
colors_cpa = ['green' if i < 5 else 'red' for i in range(len(cpa_sorted))]
ax9.barh(cpa_sorted['campana_id'], cpa_sorted['cpa'], color=colors_cpa, alpha=0.7)
ax9.set_xlabel('CPA (Costo por Acción)')
ax9.set_title('CPA por Campaña\n(Verde: Mejor, Rojo: Peor)', fontweight='bold')
ax9.axvline(x=df['cpa'].mean(), color='black', linestyle='--', linewidth=2, label=f"Promedio: {df['cpa'].mean():.2f}")
ax9.legend()

plt.tight_layout()
plt.savefig('analisis_campanas.png', dpi=300, bbox_inches='tight')
print("✅ Gráfica principal guardada como: analisis_campanas.png")

# GRÁFICA ADICIONAL: Matriz de Correlación
fig2, ax = plt.subplots(figsize=(12, 10))
numeric_df = df.select_dtypes(include=[np.number])
corr_matrix = numeric_df.corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title('Matriz de Correlación de Variables', fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig('matriz_correlacion.png', dpi=300, bbox_inches='tight')
print("✅ Matriz de correlación guardada como: matriz_correlacion.png")

# GRÁFICA ADICIONAL: Timeline de Campaigns
fig3, ax = plt.subplots(figsize=(14, 8))
df_sorted = df.sort_values('fecha_campana')
ax.plot(df_sorted['fecha_campana'], df_sorted['revenue_generado'], marker='o', linewidth=2, markersize=8, label='Revenue', color='green')
ax2_twin = ax.twinx()
ax2_twin.plot(df_sorted['fecha_campana'], df_sorted['costo_total'], marker='s', linewidth=2, markersize=8, label='Costo', color='red', linestyle='--')
ax.set_xlabel('Fecha de Campaña', fontweight='bold')
ax.set_ylabel('Revenue Generado ($)', fontweight='bold', color='green')
ax2_twin.set_ylabel('Costo Total ($)', fontweight='bold', color='red')
ax.set_title('Timeline: Revenue vs Costo por Fecha de Campaña', fontweight='bold', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left')
ax2_twin.legend(loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('timeline_campanas.png', dpi=300, bbox_inches='tight')
print("✅ Timeline de campañas guardada como: timeline_campanas.png")

print("\n" + "="*50)
print("RESUMEN DE GRÁFICAS GENERADAS:")
print("="*50)
print("1. analisis_campanas.png - Dashboard con 9 gráficas de análisis integral")
print("2. matriz_correlacion.png - Heatmap de correlaciones entre variables")
print("3. timeline_campanas.png - Evolución temporal de revenue vs costo")
print("\nTodas las gráficas han sido guardadas en la carpeta del proyecto.")
