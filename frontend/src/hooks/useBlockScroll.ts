import { useEffect } from 'react';

const useBlockScroll = (block: boolean) => {
  useEffect(() => {
    const handleScroll = (e: Event) => {
      if (block) {
        e.preventDefault();
      }
    };

    if (block) {
      document.body.style.overflow = 'hidden';
      document.addEventListener('scroll', handleScroll, { passive: false });
    } else {
      document.body.style.overflow = 'unset';
      document.removeEventListener('scroll', handleScroll);
    }

    return () => {
      document.body.style.overflow = 'unset';
      document.removeEventListener('scroll', handleScroll);
    };
  }, [block]);
};

export default useBlockScroll;
