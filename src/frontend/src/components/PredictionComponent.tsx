import React, { useState, useEffect, useMemo, Fragment } from 'react';
import { Combobox, Dialog, Transition } from '@headlessui/react';
import { ChevronUpDownIcon, CheckIcon, XMarkIcon } from '@heroicons/react/20/solid';
import debounce from 'lodash.debounce';

interface PredictionResponse {
  prediction: number;
}

const PredictionCard: React.FC = () => {
  const [knrList, setKnrList] = useState<string[]>([]);
  const [selectedKnr, setSelectedKnr] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [predictionResult, setPredictionResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://100.29.57.65:8001';

  // Debounced fetch function
  const fetchKnrs = useMemo(
    () =>
      debounce(async (searchTerm: string) => {
        if (!searchTerm) {
          setKnrList([]);
          return;
        }
        try {
          const response = await fetch(`${backendUrl}/knrs?search=${encodeURIComponent(searchTerm)}`);
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          const data = await response.json();
          if (data.knrs && Array.isArray(data.knrs)) {
            setKnrList(data.knrs);
          } else {
            console.error('Invalid KNRs data:', data);
            setKnrList([]);
          }
        } catch (error) {
          console.error('Error fetching KNRs:', error);
          setKnrList([]);
        }
      }, 300),
    [backendUrl]
  );

  useEffect(() => {
    fetchKnrs(query);

    return () => {
      fetchKnrs.cancel();
    };
  }, [query, fetchKnrs]);

  const handlePredict = () => {
    if (!selectedKnr) {
      alert('Please select a KNR');
      return;
    }
    setLoading(true);

    fetch(`${backendUrl}/predict/${selectedKnr}`, {
      method: 'POST',
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setPredictionResult(data);
        setIsModalOpen(true); // Open the modal when prediction result is received
      })
      .catch((error) => {
        console.error('Error making prediction:', error);
        alert('An error occurred while making the prediction.');
      })
      .finally(() => {
        setLoading(false);
      });
  };

  // Format the prediction result as a percentage
  const formattedPrediction = useMemo(() => {
    if (predictionResult && typeof predictionResult.prediction === 'number') {
      const percentage = predictionResult.prediction * 100;
      return percentage.toFixed(2); // Format to two decimal places
    }
    return null;
  }, [predictionResult]);

  return (
    <div className="max-w-md mx-auto mt-10">
      <div className="bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-4">Make a Prediction</h1>
        <Combobox
          value={selectedKnr}
          onChange={(value) => {
            setSelectedKnr(value);
            setQuery(value || '');
          }}
        >
          <div className="relative mb-4">
            <Combobox.Label className="block text-gray-700 mb-2">Select KNR:</Combobox.Label>
            <div className="relative w-full text-left bg-white rounded-lg shadow-md cursor-default focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              <Combobox.Input
                className="w-full border border-gray-300 rounded-md py-2 pl-3 pr-10 text-sm leading-5 text-gray-900 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Start typing to search..."
              />
              <Combobox.Button className="absolute inset-y-0 right-0 flex items-center pr-2">
                <ChevronUpDownIcon className="w-5 h-5 text-gray-400" aria-hidden="true" />
              </Combobox.Button>
            </div>
            <Transition
              as={Fragment}
              leave="transition ease-in duration-100"
              leaveFrom="opacity-100"
              leaveTo="opacity-0"
              afterLeave={() => setQuery(selectedKnr || '')}
            >
              <Combobox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto bg-white rounded-md py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                {knrList.length === 0 && query !== '' ? (
                  <div className="cursor-default select-none py-2 px-4 text-gray-700">
                    No KNR found.
                  </div>
                ) : (
                  knrList.map((knr) => (
                    <Combobox.Option
                      key={knr}
                      className={({ active }) =>
                        `cursor-default select-none relative py-2 pl-10 pr-4 ${
                          active ? 'text-white bg-[#000475]' : 'text-gray-900'
                        }`
                      }
                      value={knr}
                    >
                      {({ selected, active }) => (
                        <>
                          <span
                            className={`block truncate ${
                              selected ? 'font-medium' : 'font-normal'
                            }`}
                          >
                            {knr}
                          </span>
                          {selected ? (
                            <span
                              className={`absolute inset-y-0 left-0 flex items-center pl-3 ${
                                active ? 'text-white' : 'text-blue-600'
                              }`}
                            >
                              <CheckIcon className="w-5 h-5" aria-hidden="true" />
                            </span>
                          ) : null}
                        </>
                      )}
                    </Combobox.Option>
                  ))
                )}
              </Combobox.Options>
            </Transition>
          </div>
        </Combobox>
        <button
          onClick={handlePredict}
          disabled={loading || !selectedKnr}
          className={`w-full bg-[#000475] hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ${
            loading || !selectedKnr ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {loading ? 'Predicting...' : 'Predict'}
        </button>
      </div>

      {/* Modal to display the prediction percentage */}
      <Transition appear show={isModalOpen} as={Fragment}>
        <Dialog as="div" className="relative z-50" onClose={() => setIsModalOpen(false)}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black bg-opacity-25" />
          </Transition.Child>

          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4 text-center">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <Dialog.Panel className="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                  <button
                    className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
                    onClick={() => setIsModalOpen(false)}
                  >
                    <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                  </button>
                  <Dialog.Title
                    as="h3"
                    className="text-lg font-medium leading-6 text-gray-900 mb-4"
                  >
                    Probabilidade de Falha
                  </Dialog.Title>
                  <div className="mt-2">
                    {formattedPrediction !== null ? (
                      <p className="text-3xl font-bold text-center">
                        {formattedPrediction}% 
                      </p>
                    ) : (
                      <p className="text-gray-500">Predição não disponível.</p>
                    )}
                  </div>
                  <div className="mt-6">
                    <button
                      type="button"
                      className="w-full inline-flex justify-center rounded-md border border-transparent bg-[#000475] px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                      onClick={() => setIsModalOpen(false)}
                    >
                      Fechar
                    </button>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
    </div>
  );
};

export default PredictionCard;
