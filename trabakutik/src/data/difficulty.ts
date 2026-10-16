export type DiffKey = "low" | "mid" | "high";

/** Esfuerzo físico: calculado a partir de km + desnivel (e-bike pondera menos). */
export const effortLabel: Record<DiffKey, { es: string; eu: string }> = {
  low: { es: "Suave", eu: "Arina" },
  mid: { es: "Exigente", eu: "Nekeza" },
  high: { es: "Muy exigente", eu: "Oso nekeza" },
};

/** Terreno: calculado a partir de la superficie (sendero/pista/carretera) y la actividad. */
export const terrainLabel: Record<DiffKey, { es: string; eu: string }> = {
  low: { es: "Sencillo", eu: "Erraza" },
  mid: { es: "Medio", eu: "Ertaina" },
  high: { es: "Técnico", eu: "Teknikoa" },
};
