import React from "react";

export interface NavbarProps {
  title?: string;
}

export const Navbar: React.FC<NavbarProps> = ({ title = "MOVINT Field Intelligence" }) => {
  return (
    <nav className="navbar bg-slate-900 text-white p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">{title}</h1>
      <h1>
        kunal
      </h1>
    </nav>
  );
};

export default Navbar;
