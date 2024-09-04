import { useState } from "react";
import { GrClose } from "react-icons/gr";
import { GiHamburgerMenu } from "react-icons/gi";

const Header: React.FC = () => {
  const [showMenu, setShowMenu] = useState<boolean>(false);

  return (
    <header className="flex flex-row items-center justify-between p-4 bg-white shadow-lg">
      <a
        href="/"
        className="text-2xl font-bold italic text-black hover:opacity-90 transition-opacity duration-300"
      >
        MySite
      </a>
      <nav className="hidden sm:flex gap-8 font-medium text-black">
        <a href="#" className="hover:text-gray-300 transition-colors duration-300">
          Home
        </a>
        <a href="#" className="hover:text-gray-300 transition-colors duration-300">
          About
        </a>
        <a href="#" className="hover:text-gray-300 transition-colors duration-300">
          Contact
        </a>
      </nav>
      <nav className="sm:hidden flex items-center">
        <button
          onClick={() => setShowMenu(!showMenu)}
          className="text-2xl text-black hover:text-gray-300 transition-colors duration-300"
        >
          {showMenu ? <GrClose /> : <GiHamburgerMenu />}
        </button>
        {showMenu && (
          <div className="absolute top-16 right-4 bg-black shadow-lg rounded-lg p-4">
            <a href="#" className="block py-2 text-gray-800 hover:text-blue-600">
              Home
            </a>
            <a href="#" className="block py-2 text-gray-800 hover:text-blue-600">
              About
            </a>
            <a href="#" className="block py-2 text-gray-800 hover:text-blue-600">
              Contact
            </a>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;
