import React, { useState } from 'react';

interface DateFilterProps {
  onFilter: (startDate: string | null, endDate: string | null) => void;
}

const DateFilter: React.FC<DateFilterProps> = ({ onFilter }) => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleFilter = () => {
    if (startDate && endDate) {
      onFilter(startDate, endDate);
    } else {
      onFilter(null, null);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md flex flex-col md:flex-row items-end md:items-center space-y-4 md:space-y-0 md:space-x-6">
      <div className="flex flex-col w-full md:w-auto">
        <label className="text-gray-700 font-semibold">Start Date</label>
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="mt-2 p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#2f94bf] transition duration-200 ease-in-out"
        />
      </div>

      <div className="flex flex-col w-full md:w-auto">
        <label className="text-gray-700 font-semibold">End Date</label>
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="mt-2 p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#2f94bf] transition duration-200 ease-in-out"
        />
      </div>

      <button
        onClick={handleFilter}
        className="w-full md:w-auto bg-[#2f94bf] text-white px-6 py-3 rounded-md hover:bg-[#277b9d] transition duration-300 ease-in-out font-semibold shadow-md md:ml-4"
      >
        Apply Filter
      </button>
    </div>
  );
};

export default DateFilter;
