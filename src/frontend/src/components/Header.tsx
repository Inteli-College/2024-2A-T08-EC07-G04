import React, { useState } from 'react';

const Header: React.FC = () => {
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-md text-gray-800">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        {/* Menu Hambúrguer */}
        <div className="flex items-center md:hidden">
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="focus:outline-none"
            aria-label="Menu"
          >
            <svg
              className="w-6 h-6 text-gray-800"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h16m-7 6h7"
              ></path>
            </svg>
          </button>
          {isMenuOpen && (
            <nav className="absolute top-16 left-0 w-full bg-white text-gray-800 rounded-lg shadow-lg py-2 md:hidden">
              <a
                href="/upload"
                className="block px-4 py-2 hover:bg-gray-200"
                onClick={() => setIsMenuOpen(false)}
              >
                Upload
              </a>
            </nav>
          )}
        </div>

        {/* Logo */}
        <div className="text-center flex-1">
          <a href="/" className="text-2xl font-bold">
            Minha Logo
          </a>
        </div>

        {/* Menu para telas grandes */}
        <nav className="hidden md:flex ml-4">
          <a href="/upload" className="text-gray-800 hover:text-gray-600">
            Upload
          </a>
        </nav>

        {/* Login de Usuário */}
        <div className="relative">
          <button
            onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
            className="focus:outline-none"
          >
            <span className="text-gray-800">Login</span>
          </button>
          {isUserMenuOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white text-gray-800 rounded-lg shadow-lg py-2">
              <a
                href="/profile"
                className="block px-4 py-2 hover:bg-gray-200"
                onClick={() => setIsUserMenuOpen(false)}
              >
                Perfil
              </a>
              <a
                href="/logout"
                className="block px-4 py-2 hover:bg-gray-200"
                onClick={() => setIsUserMenuOpen(false)}
              >
                Logout
              </a>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
