// AppContext.tsx
import React, { useState } from 'react';

interface AppContextInterface {
    currentPage: string;
    setCurrentPage: React.Dispatch<React.SetStateAction<string>>;
}

const initialAppState: AppContextInterface = {
    currentPage: '',
    setCurrentPage: () => {}
};

export const AppContext = React.createContext<AppContextInterface>(initialAppState);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [currentPage, setCurrentPage] = useState<string>('');

    return (
        <AppContext.Provider value={{ currentPage, setCurrentPage }}>
            {children}
        </AppContext.Provider>
    );
};
