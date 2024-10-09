import React from 'react';

const LoginForm: React.FC = () => {
  return (
    <div className="bg-[#FAFAFA] py-12 px-24 rounded-3xl shadow-xl max-w-4xl w-full">
      <div className="max-w-sm mx-auto">
        <div className="flex justify-center mb-6">
          <img
            src="/logo.svg"
            alt="Logo"
            className="w-64 object-contain mb-4"
          />
        </div>

        <div className="mb-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <img
                src="/user.svg"
                alt="Email Icon"
                className="w-8 text-gray-400"
              />
            </div>
            <input
              className="shadow indent-10 text-2xl focus:bg-slate-400 appearance-none border-[2.5px] border-[#000475] rounded-full w-full py-[11px] px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="email"
              type="email"
              placeholder=""
            />
          </div>
        </div>

        <div className="mb-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <img
                src="/password.svg"
                alt="Password Icon"
                className="w-8 text-gray-400"
              />
            </div>
            <input
              className="shadow indent-10 text-2xl focus:bg-slate-400 appearance-none border-[2.5px] border-[#000475] rounded-full w-full py-[11px] px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="password"
              type="password"
              placeholder=""
            />
          </div>
        </div>

        <div className="mb-8">
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              className="form-checkbox border-1 border-[#000475] text-[#000475] h-4 w-4 ms-4"
            />
            <span className="ml-2 text-[#000475] ">Remember me</span>
          </label>
        </div>

        <div className="flex items-center justify-between">
          <button
            className="text-2xl appearance-none border-[2.5px] bg-[#000475] duration-700 hover:bg-slate-400 hover:text-[#000475] rounded-full text-white py-[11px] px-4 focus:outline-none focus:shadow-outline w-full"
            type="button"
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
