import React, { useState } from 'react';

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-md text-gray-800">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center">
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
        </div>

        <div
          className={`fixed inset-y-0 left-0 transform ${
            isMenuOpen ? 'translate-x-0' : '-translate-x-full'
          } transition-transform duration-300 ease-in-out bg-white w-64 shadow-lg z-50`}
        >
          <button
            onClick={() => setIsMenuOpen(false)}
            className="absolute top-4 right-4 focus:outline-none"
            aria-label="Close menu"
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
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          <nav className="mt-16">
            <a
              href="/upload"
              className="block px-4 py-2 hover:bg-gray-200"
              onClick={() => setIsMenuOpen(false)}
            >
              Retreinamento
            </a>
            <a
              href="/predict"
              className="block px-4 py-2 hover:bg-gray-200"
              onClick={() => setIsMenuOpen(false)}
            >
              Predição
            </a>
            <a
              href="/dashboard"
              className="block px-4 py-2 hover:bg-gray-200"
              onClick={() => setIsMenuOpen(false)}
            >
              Dashboard
            </a>
          </nav>
        </div>

        <div className="flex justify-center items-center">
          <a href="/">
            <img
              src="https://inteli-college.github.io/2024-2A-T08-EC07-G04/img/logo_fillmore.png"
              alt="Logo"
              width="100"
            />
          </a>
        </div>

        <div className="relative">
          <a
            href="/login"
            className="focus:outline-none text-gray-800"
          >
            User
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;
