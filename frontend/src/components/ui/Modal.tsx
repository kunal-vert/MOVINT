import React from "react";

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="modal-content bg-white rounded-lg p-6 max-w-md w-full">
        <div className="modal-header flex justify-between items-center mb-4">
          {title && <h3 className="text-lg font-semibold">{title}</h3>}
          <button onClick={onClose} className="modal-close text-gray-500 hover:text-black">
            &times;
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
