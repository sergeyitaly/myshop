import { useState, useEffect } from 'react';

const useFetch = <T>(fetchData: () => Promise<T>, deps: any[] = []): [T | null, boolean, Error | null] => {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        let isMounted = true; // Flag to check if component is mounted

        const fetchDataAsync = async () => {
            setLoading(true);
            setError(null);
            try {
                const result = await fetchData();
                if (isMounted) {
                    setData(result);
                }
            } catch (error) {
                if (isMounted) {
                    setError(error as Error);
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };

        fetchDataAsync();

        return () => {
            isMounted = false; // Cleanup flag on unmount
        };
    }, deps); // Run effect when dependencies change

    return [data, loading, error];
};

export default useFetch;
