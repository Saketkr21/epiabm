#ifndef EPIABM_DATACLASSES_POPULATION_HPP
#define EPIABM_DATACLASSES_POPULATION_HPP

#include "cell.hpp"

#include <functional>
#include <vector>
#include <memory>

namespace epiabm
{
    
    class Population
    {
    private:
        std::vector<Cell> m_cells;
        
    public:
        Population();
        ~Population() = default;

        void forEachCell(std::function<bool(Cell*)> callback);
        std::vector<Cell>& cells();
    
    private:
    };

    typedef std::shared_ptr<Population> PopulationPtr;
    
} // namespace epiabm

#endif // EPIABM_DATACLASSES_POPULATION_HPP