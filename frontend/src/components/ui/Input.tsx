import React from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, className = "", ...props }) => {
  return (
    <div className="input-wrapper">
      {label && <label className="input-label">{label}</label>}
      <input className={`input ${className}`.trim()} {...props} />
      {error && <span className="input-error text-red-500 text-xs">{error}</span>}
    </div>
  );
};

export default Input;
