// Production Design Tokens — India-First Legal & Property Intelligence Platform

export const tokens = {
  colors: {
    surfaces: {
      default: "#FAFAFA",
      raised: "#FFFFFF",
      overlay: "#F3F4F6",
      muted: "#E5E7EB",
      dark: "#0F172A",
    },
    brand: {
      primary: "#0F172A", // Deep Navy - Trust & Legal Authority
      primaryHover: "#1E293B",
      primaryActive: "#334155",
      accent: "#2563EB",  // Royal Blue - Interactive Focus
      accentHover: "#1D4ED8",
    },
    text: {
      primary: "#0F172A",
      secondary: "#475569",
      muted: "#64748B",
      disabled: "#94A3B8",
      inverse: "#FFFFFF",
    },
    badges: {
      sourceFactBg: "#EFF6FF",
      sourceFactFg: "#1E40AF",
      aiExtractionBg: "#FEF3C7",
      aiExtractionFg: "#92400E",
      humanVerifiedBg: "#F0FDF4",
      humanVerifiedFg: "#166534",
      rejectedBg: "#FEF2F2",
      rejectedFg: "#991B1B",
    },
    highlights: {
      citationFill: "rgba(254, 240, 138, 0.5)", // Yellow 200 at 50% opacity
      citationBorder: "#CA8A04",                // Yellow 600
    },
    status: {
      success: "#16A34A",
      warning: "#D97706",
      error: "#DC2626",
      info: "#2563EB",
    },
    border: {
      default: "#E2E8F0",
      strong: "#CBD5E1",
      focus: "#2563EB",
    },
  },
  typography: {
    fontSans: "'Inter', 'Noto Sans Indic', -apple-system, BlinkMacSystemFont, sans-serif",
    fontMono: "'JetBrains Mono', 'Fira Code', monospace",
    sizes: {
      xs: "0.75rem",    // 12px
      sm: "0.875rem",   // 14px
      base: "1rem",     // 16px
      lg: "1.125rem",   // 18px
      xl: "1.25rem",    // 20px
      2xl: "1.5rem",    // 24px
      3xl: "1.875rem",  // 30px
    },
    weights: {
      regular: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
  spacing: {
    xs: "0.25rem",   // 4px
    sm: "0.5rem",    // 8px
    md: "0.75rem",   // 12px
    lg: "1rem",      // 16px
    xl: "1.5rem",    // 24px
    2xl: "2rem",     // 32px
    3xl: "3rem",     // 48px
  },
  radii: {
    sm: "0.25rem",   // 4px
    md: "0.375rem",  // 6px
    lg: "0.5rem",    // 8px
    full: "9999px",
  },
  shadows: {
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
  },
  breakpoints: {
    mobile: "767px",
    tablet: "1023px",
    desktop: "1024px",
    wide: "1440px",
  },
} as const;
