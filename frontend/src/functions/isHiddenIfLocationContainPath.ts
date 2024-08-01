export const isHiddenIfLocationContainPath = (path: string, forbiddenPath: string): boolean => {

    console.log(path.split('/'));
    


    return path.split('/').includes(forbiddenPath)
}