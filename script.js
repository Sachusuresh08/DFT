document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const selectFileBtn = document.getElementById('selectFileBtn');
    const resultsSection = document.getElementById('results');
    const fileNameDisplay = document.getElementById('fileName');
    const metadataTable = document.getElementById('metadataTable');
    const noMetadataDisplay = document.getElementById('noMetadata');
    const errorMessage = document.getElementById('errorMessage');
    const resetBtn = document.getElementById('resetBtn');
    
    // Trigger file input when clicking the button or drop area
    selectFileBtn.addEventListener('click', () => fileInput.click());
    dropArea.addEventListener('click', () => fileInput.click());
    
    // Handle file selection
    fileInput.addEventListener('change', handleFiles);
    
    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('active');
    }
    
    function unhighlight() {
        dropArea.classList.remove('active');
    }
    
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length) {
            fileInput.files = files;
            handleFiles();
        }
    }
    
    // Reset functionality
    resetBtn.addEventListener('click', reset);
    
    function reset() {
        fileInput.value = '';
        resultsSection.classList.add('hidden');
        resetBtn.classList.add('hidden');
        noMetadataDisplay.classList.add('hidden');
        errorMessage.classList.add('hidden');
        metadataTable.innerHTML = '';
    }
    
    // Main processing function
    function handleFiles() {
        const file = fileInput.files[0];
        if (!file) return;
        
        // Validate file type
        if (!file.type.match('image.*')) {
            errorMessage.textContent = 'Please select an image file (JPEG, PNG, etc.)';
            errorMessage.classList.remove('hidden');
            return;
        }
        
        errorMessage.classList.add('hidden');
        fileNameDisplay.textContent = file.name;
        
        // Display loading state
        metadataTable.innerHTML = '<tr><td colspan="2" class="px-6 py-4 text-center">Loading metadata...</td></tr>';
        resultsSection.classList.remove('hidden');
        
        const reader = new FileReader();
        reader.onload = function(e) {
            // Use EXIF.js to read metadata
            EXIF.getData(file, function() {
                const allMetaData = EXIF.getAllTags(this);
                
                metadataTable.innerHTML = '';
                
                if (!allMetaData || Object.keys(allMetaData).length === 0) {
                    noMetadataDisplay.classList.remove('hidden');
                } else {
                    noMetadataDisplay.classList.add('hidden');
                    Object.entries(allMetaData).forEach(([tag, value]) => {
                        if (value !== undefined) {
                            const row = document.createElement('tr');
                            const tagCell = document.createElement('td');
                            const valueCell = document.createElement('td');
                            
                            tagCell.className = 'px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900';
                            valueCell.className = 'px-6 py-4 whitespace-nowrap text-sm text-gray-500';
                            
                            tagCell.textContent = tag;
                            valueCell.textContent = formatExifValue(value);
                            
                            row.appendChild(tagCell);
                            row.appendChild(valueCell);
                            metadataTable.appendChild(row);
                        }
                    });
                }
                
                resetBtn.classList.remove('hidden');
            });
        };
        
        reader.readAsArrayBuffer(file);
    }
    
    // Format EXIF values for better display
    function formatExifValue(value) {
        if (Array.isArray(value)) {
            return value.join(', ');
        }
        return value;
    }
});
