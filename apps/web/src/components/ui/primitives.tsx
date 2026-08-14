// Reusable UI Component Primitives — Production Design System

import React, { useState } from "react";
import { tokens } from "../../tokens";

// 1. Button Primitive
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  isLoading = false,
  disabled,
  className = "",
  style,
  ...props
}) => {
  const baseStyle: React.CSSProperties = {
    fontFamily: tokens.typography.fontSans,
    fontWeight: tokens.typography.weights.medium,
    borderRadius: tokens.radii.md,
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: disabled || isLoading ? "not-allowed" : "pointer",
    transition: "all 0.15s ease",
    border: "1px solid transparent",
    outline: "none",
    opacity: disabled ? 0.6 : 1,
  };

  const variantStyles: Record<string, React.CSSProperties> = {
    primary: {
      backgroundColor: tokens.colors.brand.primary,
      color: tokens.colors.text.inverse,
    },
    secondary: {
      backgroundColor: tokens.colors.surfaces.overlay,
      color: tokens.colors.text.primary,
      borderColor: tokens.colors.border.default,
    },
    outline: {
      backgroundColor: "transparent",
      color: tokens.colors.text.primary,
      borderColor: tokens.colors.border.default,
    },
    danger: {
      backgroundColor: tokens.colors.status.error,
      color: tokens.colors.text.inverse,
    },
    ghost: {
      backgroundColor: "transparent",
      color: tokens.colors.text.secondary,
    },
  };

  const sizeStyles: Record<string, React.CSSProperties> = {
    sm: { padding: "4px 12px", fontSize: tokens.typography.sizes.xs, height: "32px" },
    md: { padding: "8px 16px", fontSize: tokens.typography.sizes.sm, height: "40px" },
    lg: { padding: "12px 24px", fontSize: tokens.typography.sizes.base, height: "48px" },
  };

  return (
    <button
      disabled={disabled || isLoading}
      style={{ ...baseStyle, ...variantStyles[variant], ...sizeStyles[size], ...style }}
      className={`focus:ring-2 focus:ring-blue-600 ${className}`}
      {...props}
    >
      {isLoading ? <span style={{ marginRight: "8px" }}>⏳ Loading...</span> : null}
      {children}
    </button>
  );
};

// 2. Input Primitive
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, helperText, className = "", style, ...props }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: tokens.spacing.xs, width: "100%" }}>
      {label && (
        <label style={{ fontSize: tokens.typography.sizes.xs, fontWeight: tokens.typography.weights.medium, color: tokens.colors.text.secondary }}>
          {label}
        </label>
      )}
      <input
        style={{
          height: "40px",
          padding: "0 12px",
          borderRadius: tokens.radii.md,
          border: `1px solid ${error ? tokens.colors.status.error : tokens.colors.border.default}`,
          backgroundColor: tokens.colors.surfaces.raised,
          fontSize: tokens.typography.sizes.sm,
          color: tokens.colors.text.primary,
          outline: "none",
          ...style,
        }}
        {...props}
      />
      {error && <span style={{ fontSize: tokens.typography.sizes.xs, color: tokens.colors.status.error }}>{error}</span>}
      {helperText && !error && <span style={{ fontSize: tokens.typography.sizes.xs, color: tokens.colors.text.muted }}>{helperText}</span>}
    </div>
  );
};

// 3. Badge Primitive
export interface BadgeProps {
  variant: "SOURCE_FACT" | "AI_EXTRACTION" | "AI_INFERENCE" | "HUMAN_VERIFIED" | "REJECTED" | "CRITICAL" | "WARNING" | "INFO";
  children: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({ variant, children }) => {
  const badgeStyles: Record<string, React.CSSProperties> = {
    SOURCE_FACT: { backgroundColor: tokens.colors.badges.sourceFactBg, color: tokens.colors.badges.sourceFactFg },
    AI_EXTRACTION: { backgroundColor: tokens.colors.badges.aiExtractionBg, color: tokens.colors.badges.aiExtractionFg },
    AI_INFERENCE: { backgroundColor: "#F3E8FF", color: "#6B21A8" },
    HUMAN_VERIFIED: { backgroundColor: tokens.colors.badges.humanVerifiedBg, color: tokens.colors.badges.humanVerifiedFg },
    REJECTED: { backgroundColor: tokens.colors.badges.rejectedBg, color: tokens.colors.badges.rejectedFg },
    CRITICAL: { backgroundColor: "#FEE2E2", color: "#991B1B" },
    WARNING: { backgroundColor: "#FEF3C7", color: "#92400E" },
    INFO: { backgroundColor: "#E0F2FE", color: "#075985" },
  };

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "2px 8px",
        borderRadius: tokens.radii.full,
        fontSize: "11px",
        fontWeight: tokens.typography.weights.semibold,
        letterSpacing: "0.05em",
        textTransform: "uppercase",
        ...badgeStyles[variant],
      }}
    >
      {children}
    </span>
  );
};

// 4. Modal Primitive
export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(15, 23, 42, 0.6)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
      role="dialog"
      aria-modal="true"
    >
      <div
        style={{
          backgroundColor: tokens.colors.surfaces.raised,
          borderRadius: tokens.radii.lg,
          padding: tokens.spacing.xl,
          width: "90%",
          maxWidth: "540px",
          boxShadow: tokens.shadows.lg,
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: tokens.spacing.lg }}>
          <h3 style={{ margin: 0, fontSize: tokens.typography.sizes.lg, fontWeight: tokens.typography.weights.semibold }}>{title}</h3>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", fontSize: "18px" }} aria-label="Close Modal">
            ✕
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
};

// 5. Card Container
export const Card: React.FC<{ children: React.ReactNode; className?: string; style?: React.CSSProperties }> = ({ children, style }) => (
  <div
    style={{
      backgroundColor: tokens.colors.surfaces.raised,
      borderRadius: tokens.radii.lg,
      border: `1px solid ${tokens.colors.border.default}`,
      padding: tokens.spacing.lg,
      boxShadow: tokens.shadows.sm,
      ...style,
    }}
  >
    {children}
  </div>
);
