

export const transformURL = (src: string): string => {
    
    
    if(!import.meta.env.DEV) return src

    return src.split('/')[0] ? src : import.meta.env.VITE_LOCAL_API_BASE_URL + src
}